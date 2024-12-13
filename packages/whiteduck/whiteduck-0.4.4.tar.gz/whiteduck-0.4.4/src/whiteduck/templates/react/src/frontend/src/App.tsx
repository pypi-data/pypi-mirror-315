import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from './components/ui/card';
import { Button } from './components/ui/button';
import { useState } from 'react';

interface SystemInfo {
  os: {
    name: string;
    version: string;
    machine: string;
    processor: string;
  };
  memory: {
    total: string;
    available: string;
    percent_used: number;
  };
  cpu: {
    cores: number;
    physical_cores: number;
    current_frequency: string;
    usage_percent: number;
  };
  system: {
    boot_time: string;
    python_version: string;
  };
}

function App() {
  const [systemInfo, setSystemInfo] = useState<SystemInfo | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSystemInfo = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch('http://127.0.0.1:8000/api/system_info');
      const data = await response.json();
      setSystemInfo(data);
    } catch (err) {
      setError('Failed to fetch system information');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="mb-8">
        <img src="/wd.png" alt="Project Logo" className="max-w-[200px] h-auto" />
      </div>

      <Card className="w-full max-w-2xl">
        <CardHeader>
          <CardTitle>Frontend template for python projects</CardTitle>
          <CardDescription>Your journey starts here.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <p>Vite + React + Typescript + ShadCn</p>

          {error && (
            <p className="text-red-500 mt-2">{error}</p>
          )}

          {systemInfo && (
            <div className="mt-4 space-y-4">
              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="font-semibold mb-2">Operating System</h3>
                <p>Name: {systemInfo.os.name}</p>
                <p>Version: {systemInfo.os.version}</p>
                <p>Machine: {systemInfo.os.machine}</p>
                <p>Processor: {systemInfo.os.processor}</p>
              </div>

              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="font-semibold mb-2">Memory</h3>
                <p>Total: {systemInfo.memory.total}</p>
                <p>Available: {systemInfo.memory.available}</p>
                <p>Used: {systemInfo.memory.percent_used}%</p>
              </div>

              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="font-semibold mb-2">CPU</h3>
                <p>Cores: {systemInfo.cpu.cores}</p>
                <p>Physical Cores: {systemInfo.cpu.physical_cores}</p>
                <p>Current Frequency: {systemInfo.cpu.current_frequency}</p>
                <p>Usage: {systemInfo.cpu.usage_percent}%</p>
              </div>

              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="font-semibold mb-2">System</h3>
                <p>Boot Time: {systemInfo.system.boot_time}</p>
                <p>Python Version: {systemInfo.system.python_version}</p>
              </div>
            </div>
          )}
        </CardContent>
        <CardFooter className="flex justify-end">
          <Button
            onClick={fetchSystemInfo}
            disabled={loading}
          >
            {loading ? 'Loading...' : 'Get System Info'}
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}

export default App;
