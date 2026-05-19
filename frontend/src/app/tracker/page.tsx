"use client";

export default function TrackerPage() {
  const columns = [
    { title: "Shortlisted", items: ["Frontend Engineer @ Stripe", "React Dev @ Vercel"] },
    { title: "Tailoring Resume", items: ["Full Stack @ Meta"] },
    { title: "Applied", items: ["UI Engineer @ Apple", "Software Dev @ Amazon"] },
    { title: "Interviewing", items: ["Frontend Dev @ Google"] },
    { title: "Rejected/Ghosted", items: ["Web Dev @ StartupX"] }
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex">
      <main className="flex-1 p-8">
        <header className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900">Application Tracker</h2>
          <p className="text-gray-600 mt-1">Manage your job pipeline visually.</p>
        </header>

        <div className="flex space-x-4 overflow-x-auto pb-4">
          {columns.map((col, i) => (
            <div key={i} className="min-w-[300px] bg-gray-100/50 rounded-xl p-4 border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-gray-700">{col.title}</h3>
                <span className="bg-gray-200 text-gray-600 text-xs font-bold px-2 py-1 rounded-full">{col.items.length}</span>
              </div>
              <div className="space-y-3">
                {col.items.map((item, j) => (
                  <div key={j} className="bg-white p-4 rounded-lg shadow-sm border border-gray-100 cursor-pointer hover:border-blue-300 transition-colors">
                    <p className="font-medium text-gray-900">{item.split(' @ ')[0]}</p>
                    <p className="text-sm text-gray-500">{item.split(' @ ')[1]}</p>
                    <div className="mt-3 flex items-center justify-between">
                      <span className="text-xs text-gray-400">Updated 2d ago</span>
                      <button className="text-blue-600 hover:text-blue-800 text-xs font-medium">View &rarr;</button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
