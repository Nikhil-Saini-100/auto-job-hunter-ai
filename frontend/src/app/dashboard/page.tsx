"use client";

import Link from "next/link";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar Navigation */}
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col hidden md:flex">
        <div className="p-6">
          <h1 className="text-xl font-bold text-gray-900 tracking-tight">Auto Job Hunter</h1>
        </div>
        <nav className="flex-1 px-4 space-y-2">
          <Link href="/dashboard" className="flex items-center px-4 py-2 text-sm font-medium text-blue-700 bg-blue-50 rounded-lg">
            Dashboard
          </Link>
          <Link href="/profile" className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg">
            Profile & Resume
          </Link>
          <Link href="/discovery" className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg">
            Job Discovery
          </Link>
          <Link href="/tracker" className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg">
            Application Tracker
          </Link>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8">
        <header className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900">Welcome back, Nikhil!</h2>
          <p className="text-gray-600 mt-1">Here is a quick overview of your automated job hunting progress.</p>
        </header>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {[
            { label: "Jobs Discovered", value: "342", color: "text-blue-600" },
            { label: "Shortlisted", value: "45", color: "text-indigo-600" },
            { label: "Auto Applied", value: "12", color: "text-green-600" },
            { label: "Interviews", value: "2", color: "text-purple-600" }
          ].map((stat, i) => (
            <div key={i} className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
              <p className="text-sm font-medium text-gray-500">{stat.label}</p>
              <p className={`text-3xl font-bold mt-2 ${stat.color}`}>{stat.value}</p>
            </div>
          ))}
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Automation Activity</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-100">
              <div>
                <p className="font-medium text-gray-900">Applied to Senior Frontend Engineer at Vercel</p>
                <p className="text-sm text-gray-500">Resume Tailored & Cover Letter Generated</p>
              </div>
              <span className="px-3 py-1 text-xs font-medium text-green-700 bg-green-100 rounded-full">Success</span>
            </div>
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-100">
              <div>
                <p className="font-medium text-gray-900">Found 95% Match: Full Stack Developer at Stripe</p>
                <p className="text-sm text-gray-500">Missing skill: Go. Strengths: React, TypeScript.</p>
              </div>
              <span className="px-3 py-1 text-xs font-medium text-blue-700 bg-blue-100 rounded-full">Discovered</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
