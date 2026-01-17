import { ChatBox } from '@/components/Chat/ChatBox';
import { AgentDashboard } from '@/components/Dashboard/AgentDashboard';

export default function DemoPage() {
  return (
    <div className="min-h-screen bg-zinc-900">
      {/* Demo Chat Section */}
      <section className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-white mb-4">Chat Interface Demo</h1>
        <div className="h-[600px] bg-zinc-800 rounded-lg overflow-hidden">
          <ChatBox />
        </div>
      </section>

      {/* Demo Agent Dashboard Section */}
      <section className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-white mb-4">Agent Dashboard Demo</h1>
        <AgentDashboard />
      </section>
    </div>
  );
}
