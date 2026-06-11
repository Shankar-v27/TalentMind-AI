import { Bar, BarChart, CartesianGrid, Cell, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Card } from "../components/ui/Card";
import { analytics } from "../data/mockData";

const colors = ["#2563eb", "#7c3aed", "#0891b2", "#10b981", "#f59e0b"];

function ChartCard({ title, children }) {
  return (
    <Card>
      <h3 className="mb-4 text-lg font-extrabold">{title}</h3>
      <div className="h-72">{children}</div>
    </Card>
  );
}

export function Analytics() {
  return (
    <div className="space-y-5">
      <Card>
        <h2 className="text-2xl font-extrabold">Recruitment analytics</h2>
        <p className="mt-1 text-sm text-muted-foreground">Interactive talent pool intelligence across score distribution, location, skills, behavior, and pipeline movement.</p>
      </Card>
      <div className="grid gap-5 xl:grid-cols-2">
        <ChartCard title="Candidate score distribution">
          <ResponsiveContainer>
            <BarChart data={analytics.scoreDistribution}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
              <XAxis dataKey="bucket" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="candidates" radius={[8, 8, 0, 0]} fill="#2563eb" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
        <ChartCard title="Top skills in talent pool">
          <ResponsiveContainer>
            <BarChart data={analytics.skills} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
              <XAxis type="number" />
              <YAxis type="category" dataKey="skill" width={82} />
              <Tooltip />
              <Bar dataKey="count" radius={[0, 8, 8, 0]} fill="#7c3aed" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
        <ChartCard title="Experience distribution">
          <ResponsiveContainer>
            <BarChart data={analytics.experience}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
              <XAxis dataKey="range" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" radius={[8, 8, 0, 0]} fill="#0891b2" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
        <ChartCard title="Location distribution">
          <ResponsiveContainer>
            <PieChart>
              <Pie data={analytics.locations} dataKey="value" nameKey="name" outerRadius={95} label>
                {analytics.locations.map((entry, index) => <Cell key={entry.name} fill={colors[index % colors.length]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
        <ChartCard title="Behavioral analytics">
          <ResponsiveContainer>
            <BarChart data={analytics.behavior}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
              <XAxis dataKey="metric" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" radius={[8, 8, 0, 0]} fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
        <ChartCard title="Recruitment pipeline insights">
          <ResponsiveContainer>
            <LineChart data={analytics.pipeline}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
              <XAxis dataKey="week" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="retrieved" stroke="#2563eb" strokeWidth={3} />
              <Line type="monotone" dataKey="shortlisted" stroke="#7c3aed" strokeWidth={3} />
              <Line type="monotone" dataKey="contacted" stroke="#10b981" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>
    </div>
  );
}
