import { NextRequest, NextResponse } from 'next/server';

// Mock agent data - replace with actual agent registry
const MOCK_AGENTS = Array.from({ length: 219 }, (_, i) => ({
  id: i + 1,
  name: `Agent ${i + 1}`,
  category: ['AI/ML', 'Legal', 'Finance', 'Data', 'Code'][i % 5],
  status: ['active', 'idle'][Math.floor(Math.random() * 2)] as 'active' | 'idle',
  tasksCompleted: Math.floor(Math.random() * 1000),
  uptime: `${Math.floor(Math.random() * 24)}h ${Math.floor(Math.random() * 60)}m`,
}));

export async function GET(request: NextRequest) {
  try {
    const agents = MOCK_AGENTS;
    const active = agents.filter(a => a.status === 'active').length;
    const idle = agents.filter(a => a.status === 'idle').length;

    return NextResponse.json({
      total: 219,
      active,
      idle,
      error: 0,
      agents: agents.slice(0, 50), // Return first 50 for performance
    });
  } catch (error) {
    console.error('Agents API error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch agents' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const { agent_id, task } = await request.json();

    if (!agent_id || !task) {
      return NextResponse.json(
        { error: 'Missing agent_id or task' },
        { status: 400 }
      );
    }

    // Mock execution - replace with actual agent orchestration
    return NextResponse.json({
      agent_id,
      task,
      status: 'completed',
      output: `Task "${task}" executed successfully by Agent #${agent_id}`,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Agent execution error:', error);
    return NextResponse.json(
      { error: 'Failed to execute agent task' },
      { status: 500 }
    );
  }
}

export const runtime = 'nodejs';
