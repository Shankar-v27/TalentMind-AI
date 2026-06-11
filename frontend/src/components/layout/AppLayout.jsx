import { NavLink, Outlet, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import { BarChart3, Bot, BrainCircuit, LayoutDashboard, Moon, Search, Sparkles, Sun, UsersRound } from "lucide-react";
import { Button } from "../ui/Button";
import { useTalentMindStore } from "../../state/useTalentMindStore";
import { Copilot } from "../copilot/Copilot";

const nav = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/job-analysis", label: "JD Analysis", icon: BrainCircuit },
  { to: "/rankings", label: "Rankings", icon: UsersRound },
  { to: "/analytics", label: "Analytics", icon: BarChart3 },
];

export function AppLayout() {
  const { theme, toggleTheme } = useTalentMindStore();
  const location = useLocation();

  return (
    <div className={theme}>
      <div className="min-h-screen bg-background/70 text-foreground">
        <aside className="fixed inset-y-0 left-0 z-30 hidden w-72 border-r bg-card/70 p-5 backdrop-blur-xl lg:block">
          <div className="mb-8 flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-violet-600 text-white">
              <Sparkles size={22} />
            </div>
            <div>
              <div className="text-lg font-extrabold">TalentMind AI</div>
              <div className="text-xs font-medium text-muted-foreground">Recruitment intelligence</div>
            </div>
          </div>
          <nav className="space-y-2">
            {nav.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-lg px-3 py-3 text-sm font-semibold transition ${
                    isActive ? "bg-primary text-primary-foreground shadow-glow" : "text-muted-foreground hover:bg-muted hover:text-foreground"
                  }`
                }
              >
                <item.icon size={18} />
                {item.label}
              </NavLink>
            ))}
          </nav>
          <div className="absolute bottom-5 left-5 right-5 rounded-lg border bg-muted/50 p-4">
            <div className="mb-2 flex items-center gap-2 text-sm font-bold">
              <Bot size={17} /> AI Copilot
            </div>
            <p className="text-xs leading-5 text-muted-foreground">Natural-language discovery across 100,000 candidate profiles.</p>
          </div>
        </aside>
        <main className="lg:pl-72">
          <header className="sticky top-0 z-20 border-b bg-background/72 px-4 py-3 backdrop-blur-xl sm:px-6">
            <div className="mx-auto flex max-w-7xl items-center justify-between gap-3">
              <div className="min-w-0">
                <div className="truncate text-sm font-semibold text-muted-foreground">TalentMind Command Center</div>
                <div className="truncate text-xl font-extrabold">
                  {location.pathname === "/" ? "AI recruitment dashboard" : "Recruitment workflow"}
                </div>
              </div>
              <div className="hidden w-full max-w-sm items-center gap-2 rounded-lg border bg-card/70 px-3 py-2 md:flex">
                <Search size={16} className="text-muted-foreground" />
                <span className="text-sm text-muted-foreground">Search candidates, skills, locations</span>
              </div>
              <Button variant="outline" size="icon" onClick={toggleTheme} aria-label="Toggle theme">
                {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
              </Button>
            </div>
          </header>
          <motion.div
            key={location.pathname}
            initial={{ opacity: 0, y: 14 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25 }}
            className="mx-auto max-w-7xl p-4 sm:p-6"
          >
            <Outlet />
          </motion.div>
        </main>
        <Copilot />
      </div>
    </div>
  );
}
