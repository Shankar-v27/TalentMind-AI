import { useState } from "react";
import { NavLink, Outlet, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  LayoutDashboard, BrainCircuit, UsersRound, Clock, Sliders,
  Network, BarChart3, Search, Bell, ChevronLeft, ChevronRight,
  Sparkles, Zap, Shield, GitBranch, Users, TrendingUp, Dna,
  Activity, Settings, HelpCircle, Sun, Moon, Bot, X, Command
} from "lucide-react";
import { useTalentMindStore } from "../../state/useTalentMindStore";
import { Copilot } from "../copilot/Copilot";

const NAV_SECTIONS = [
  {
    label: "Core",
    items: [
      { to: "/",               label: "Dashboard",       icon: LayoutDashboard, pill: null },
      { to: "/job-analysis",   label: "JD Analysis",     icon: BrainCircuit,    pill: "AI" },
      { to: "/rankings",       label: "Candidate Rank",  icon: UsersRound,      pill: null },
    ],
  },
  {
    label: "Intelligence",
    items: [
      { to: "/time-machine",   label: "Time Machine",    icon: Clock,           pill: "Live" },
      { to: "/optimizer",      label: "MOHO Optimizer",  icon: Sliders,         pill: "New" },
      { to: "/recruiter-memory", label: "Memory Graph",  icon: Network,         pill: null },
    ],
  },
  {
    label: "Insights",
    items: [
      { to: "/analytics",      label: "Analytics",       icon: BarChart3,       pill: null },
    ],
  },
];

const PILL_COLORS = {
  "AI":   "pill-violet",
  "Live": "pill-emerald",
  "New":  "pill-cyan",
};

export function AppLayout() {
  const { theme, toggleTheme } = useTalentMindStore();
  const location = useLocation();
  const [collapsed, setCollapsed] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [notifOpen, setNotifOpen] = useState(false);
  const [copilotOpen, setCopilotOpen] = useState(false);

  const pageLabel = NAV_SECTIONS
    .flatMap(s => s.items)
    .find(i => i.to === location.pathname)?.label ?? "TalentMind AI";

  return (
    <div className={`${theme} flex h-screen overflow-hidden`} style={{ background: "var(--tm-bg-base)" }}>

      {/* ═══ SIDEBAR ═══ */}
      <motion.aside
        animate={{ width: collapsed ? 64 : 240 }}
        transition={{ duration: 0.25, ease: [0.4, 0, 0.2, 1] }}
        className="relative z-30 flex flex-shrink-0 flex-col border-r"
        style={{
          background: "var(--tm-bg-elevated)",
          borderColor: "var(--tm-border)",
          overflow: "hidden",
        }}
      >
        {/* Logo */}
        <div className="flex items-center gap-3 px-4 py-5 border-b" style={{ borderColor: "var(--tm-border)", minHeight: 64 }}>
          <div
            className="flex-shrink-0 flex items-center justify-center rounded-lg"
            style={{
              width: 32, height: 32,
              background: "linear-gradient(135deg, #2563EB 0%, #7C3AED 100%)",
              boxShadow: "0 0 16px rgba(37,99,235,0.4)",
            }}
          >
            <Sparkles size={16} className="text-white" />
          </div>
          <AnimatePresence>
            {!collapsed && (
              <motion.div
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -8 }}
                transition={{ duration: 0.18 }}
                className="overflow-hidden"
              >
                <div className="text-[13px] font-800 text-white leading-tight font-extrabold tracking-tight">TalentMind AI</div>
                <div className="text-[10px] font-medium" style={{ color: "var(--tm-text-muted)" }}>Human Capital Intelligence</div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Nav */}
        <nav className="flex-1 overflow-y-auto overflow-x-hidden py-3 px-2" style={{ scrollbarWidth: "none" }}>
          {NAV_SECTIONS.map((section) => (
            <div key={section.label} className="mb-4">
              <AnimatePresence>
                {!collapsed && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="px-2 py-1.5 text-[10px] font-700 font-bold tracking-widest uppercase"
                    style={{ color: "var(--tm-text-muted)" }}
                  >
                    {section.label}
                  </motion.div>
                )}
              </AnimatePresence>
              {section.items.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.to === "/"}
                  className={({ isActive }) =>
                    `sidebar-nav-item mb-0.5 ${isActive ? "active" : ""}`
                  }
                  title={collapsed ? item.label : undefined}
                >
                  <item.icon size={16} className="flex-shrink-0" />
                  <AnimatePresence>
                    {!collapsed && (
                      <motion.span
                        initial={{ opacity: 0, x: -8 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -8 }}
                        transition={{ duration: 0.15 }}
                        className="flex-1 min-w-0 truncate"
                      >
                        {item.label}
                      </motion.span>
                    )}
                  </AnimatePresence>
                  {!collapsed && item.pill && (
                    <span className={`pill ${PILL_COLORS[item.pill] ?? "pill-blue"}`} style={{ fontSize: 9, padding: "1px 6px" }}>
                      {item.pill}
                    </span>
                  )}
                </NavLink>
              ))}
            </div>
          ))}
        </nav>

        {/* Collapse toggle */}
        <div className="border-t px-2 py-3" style={{ borderColor: "var(--tm-border)" }}>
          {!collapsed && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mb-3 mx-1 rounded-lg p-3 border"
              style={{
                background: "rgba(37,99,235,0.06)",
                borderColor: "rgba(37,99,235,0.18)",
              }}
            >
              <div className="flex items-center gap-2 mb-1">
                <Bot size={13} style={{ color: "var(--tm-cyan)" }} />
                <span className="text-xs font-semibold text-white">AI Copilot</span>
              </div>
              <p className="text-[10px] leading-4" style={{ color: "var(--tm-text-muted)" }}>
                Ask anything about candidates or hiring.
              </p>
              <button
                onClick={() => setCopilotOpen(true)}
                className="btn btn-primary btn-sm mt-2 w-full text-[11px]"
              >
                Open Copilot
              </button>
            </motion.div>
          )}
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="btn btn-ghost btn-sm w-full justify-center"
          >
            {collapsed ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
          </button>
        </div>
      </motion.aside>

      {/* ═══ MAIN AREA ═══ */}
      <div className="flex flex-1 flex-col overflow-hidden min-w-0">

        {/* ─── TOP NAVBAR ─── */}
        <header
          className="flex-shrink-0 flex items-center justify-between px-5 border-b"
          style={{
            height: 56,
            background: "rgba(9,9,11,0.85)",
            backdropFilter: "blur(20px)",
            WebkitBackdropFilter: "blur(20px)",
            borderColor: "var(--tm-border)",
            zIndex: 20,
          }}
        >
          {/* Left: breadcrumb */}
          <div className="flex items-center gap-3 min-w-0">
            <div className="flex items-center gap-1.5" style={{ color: "var(--tm-text-muted)", fontSize: 12 }}>
              <Sparkles size={12} />
              <span>TalentMind</span>
              <span>/</span>
            </div>
            <span className="font-semibold text-white text-sm truncate">{pageLabel}</span>
          </div>

          {/* Center: search */}
          <button
            onClick={() => setSearchOpen(true)}
            className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-lg border transition-all"
            style={{
              background: "rgba(255,255,255,0.03)",
              borderColor: "var(--tm-border)",
              color: "var(--tm-text-muted)",
              fontSize: 13,
              width: 280,
            }}
          >
            <Search size={13} />
            <span>Search candidates, skills…</span>
            <span
              className="ml-auto flex items-center gap-1 rounded px-1.5 py-0.5 text-[10px] font-mono"
              style={{ background: "rgba(255,255,255,0.06)", color: "var(--tm-text-muted)" }}
            >
              <Command size={9} /> K
            </span>
          </button>

          {/* Right: actions */}
          <div className="flex items-center gap-1.5">
            {/* Live status */}
            <div className="hidden sm:flex items-center gap-2 px-2.5 py-1.5 rounded-lg border mr-1"
              style={{ borderColor: "rgba(16,185,129,0.2)", background: "rgba(16,185,129,0.05)", fontSize: 11 }}>
              <span className="status-dot live" />
              <span style={{ color: "#6EE7B7" }} className="font-semibold">Live</span>
            </div>

            <button
              onClick={() => setNotifOpen(!notifOpen)}
              className="btn btn-ghost btn-icon relative"
            >
              <Bell size={16} />
              <span
                className="absolute top-1 right-1 w-1.5 h-1.5 rounded-full"
                style={{ background: "#EF4444" }}
              />
            </button>

            <button onClick={toggleTheme} className="btn btn-ghost btn-icon">
              {theme === "dark" ? <Sun size={16} /> : <Moon size={16} />}
            </button>

            {/* Avatar */}
            <div
              className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white ml-1 cursor-pointer"
              style={{ background: "linear-gradient(135deg, #2563EB, #7C3AED)" }}
            >
              R
            </div>
          </div>
        </header>

        {/* ─── PAGE CONTENT ─── */}
        <main className="flex-1 overflow-y-auto overflow-x-hidden">
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -6 }}
              transition={{ duration: 0.22, ease: [0.4, 0, 0.2, 1] }}
              className="mx-auto max-w-screen-2xl p-5 pb-10"
            >
              <Outlet />
            </motion.div>
          </AnimatePresence>
        </main>
      </div>

      {/* ═══ COPILOT MODAL ═══ */}
      <AnimatePresence>
        {copilotOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-end justify-end p-4"
            style={{ background: "rgba(0,0,0,0.5)", backdropFilter: "blur(4px)" }}
            onClick={() => setCopilotOpen(false)}
          >
            <motion.div
              initial={{ opacity: 0, y: 20, scale: 0.97 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 20, scale: 0.97 }}
              onClick={(e) => e.stopPropagation()}
            >
              <Copilot onClose={() => setCopilotOpen(false)} />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ═══ SEARCH MODAL ═══ */}
      <AnimatePresence>
        {searchOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4"
            style={{ background: "rgba(0,0,0,0.6)", backdropFilter: "blur(8px)" }}
            onClick={() => setSearchOpen(false)}
          >
            <motion.div
              initial={{ opacity: 0, y: -16, scale: 0.97 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -16, scale: 0.97 }}
              className="w-full max-w-xl rounded-2xl border p-1"
              style={{ background: "var(--tm-bg-elevated)", borderColor: "var(--tm-border-bright)" }}
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center gap-3 px-4 py-3 border-b" style={{ borderColor: "var(--tm-border)" }}>
                <Search size={16} style={{ color: "var(--tm-text-muted)" }} />
                <input
                  autoFocus
                  placeholder="Search candidates, skills, roles…"
                  className="flex-1 bg-transparent text-white text-sm outline-none"
                  style={{ caretColor: "#2563EB" }}
                />
                <button onClick={() => setSearchOpen(false)} className="btn btn-ghost btn-icon btn-sm">
                  <X size={14} />
                </button>
              </div>
              <div className="px-4 py-3 text-xs" style={{ color: "var(--tm-text-muted)" }}>
                Type to search across all candidates, skills, and job descriptions…
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
