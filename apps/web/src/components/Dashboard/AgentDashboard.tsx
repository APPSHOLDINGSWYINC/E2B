'use client';

import { useState, useEffect } from 'react';
import { Activity, Cpu, Zap, AlertCircle } from 'lucide-react';

interface Agent {
  id: number;
  name: string;
  category: string;
  status: 'active' | 'idle' | 'error';
  tasksCompleted: number;
  uptime: string;
}

export function AgentDashboard() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [stats, setStats] = useState({
    total: 219,
    active: 0,
    idle: 0,
    error: 0,
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Fetch agents from API
    fetchAgents();
    const interval = setInterval(fetchAgents, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await fetch('/api/agents');
      const data = await response.json();
      setAgents(data.agents || []);
      
      // Calculate stats
      const active = data.agents?.filter((a: Agent) => a.status === 'active').length || 0;
      const idle = data.agents?.filter((a: Agent) => a.status === 'idle').length || 0;
      const error = data.agents?.filter((a: Agent) => a.status === 'error').length || 0;
      
      setStats({ total: 219, active, idle, error });
      setIsLoading(false);
    } catch (error) {
      console.error('Failed to fetch agents:', error);
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">
          AgentX5 Control Center
        </h1>
        <p className="text-purple-300">
          Orchestrating 219 AI agents for maximum productivity
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <StatCard
          icon={<Cpu className="w-8 h-8" />}
          label="Total Agents"
          value={stats.total}
          color="purple"
        />
        <StatCard
          icon={<Activity className="w-8 h-8" />}
          label="Active"
          value={stats.active}
          color="green"
        />
        <StatCard
          icon={<Zap className="w-8 h-8" />}
          label="Idle"
          value={stats.idle}
          color="yellow"
        />
        <StatCard
          icon={<AlertCircle className="w-8 h-8" />}
          label="Errors"
          value={stats.error}
          color="red"
        />
      </div>

      {/* Agent Grid */}
      {isLoading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
          <p className="text-purple-300 mt-4">Loading agents...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {agents.map((agent) => (
            <AgentCard key={agent.id} agent={agent} />
          ))}
        </div>
      )}
    </div>
  );
}

function StatCard({ icon, label, value, color }: any) {
  const colorClasses = {
    purple: 'from-purple-600 to-pink-600',
    green: 'from-green-600 to-emerald-600',
    yellow: 'from-yellow-600 to-orange-600',
    red: 'from-red-600 to-rose-600',
  };

  return (
    <div className="bg-black/40 backdrop-blur-md rounded-xl p-6 border border-purple-500/30 hover:border-purple-400/50 transition-all">
      <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${colorClasses[color]} flex items-center justify-center text-white mb-4`}>
        {icon}
      </div>
      <div className="text-3xl font-bold text-white mb-1">{value}</div>
      <div className="text-sm text-purple-300">{label}</div>
    </div>
  );
}

function AgentCard({ agent }: { agent: Agent }) {
  const statusColors = {
    active: 'bg-green-500',
    idle: 'bg-yellow-500',
    error: 'bg-red-500',
  };

  return (
    <div className="bg-black/40 backdrop-blur-md rounded-xl p-4 border border-purple-500/30 hover:border-purple-400/50 transition-all">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${statusColors[agent.status]} animate-pulse`} />
          <span className="text-sm font-medium text-white">Agent #{agent.id}</span>
        </div>
        <span className="text-xs px-2 py-1 bg-purple-500/20 text-purple-300 rounded">
          {agent.category}
        </span>
      </div>
      
      <h3 className="text-white font-semibold mb-2 truncate">{agent.name}</h3>
      
      <div className="flex items-center justify-between text-sm">
        <span className="text-purple-300">Tasks: {agent.tasksCompleted}</span>
        <span className="text-purple-300">Uptime: {agent.uptime}</span>
      </div>
    </div>
  );
}
