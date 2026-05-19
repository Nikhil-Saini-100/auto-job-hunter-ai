"use client";

import { useState } from "react";

export default function ProfilePage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    // Simulate AI parsing
    setTimeout(() => {
      setUploading(false);
      alert("Resume parsed successfully!");
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Main Content */}
      <main className="flex-1 p-8">
        <header className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900">Master Profile</h2>
          <p className="text-gray-600 mt-1">Upload your base resume and set your preferences.</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Resume Upload section */}
          <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Upload Master Resume</h3>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:bg-gray-50 transition-colors cursor-pointer">
              <input 
                type="file" 
                className="hidden" 
                id="resume-upload" 
                accept=".pdf,.docx"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
              />
              <label htmlFor="resume-upload" className="cursor-pointer">
                <p className="text-sm font-medium text-blue-600">Click to upload or drag and drop</p>
                <p className="text-xs text-gray-500 mt-1">PDF or DOCX up to 10MB</p>
                {file && <p className="mt-4 text-sm font-semibold text-gray-900">Selected: {file.name}</p>}
              </label>
            </div>
            <button 
              className={`mt-4 w-full py-2 px-4 rounded-lg font-medium text-white ${uploading ? 'bg-blue-400' : 'bg-blue-600 hover:bg-blue-700'}`}
              onClick={handleUpload}
              disabled={!file || uploading}
            >
              {uploading ? "AI is Extracting Data..." : "Upload & Parse"}
            </button>
          </div>

          {/* Preferences Section */}
          <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Job Preferences</h3>
            <form className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Preferred Roles (comma separated)</label>
                <input type="text" className="mt-1 w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" placeholder="e.g. Frontend Engineer, Full Stack Developer" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Expected Salary Range</label>
                <input type="text" className="mt-1 w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" placeholder="e.g. $100k - $150k" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Work Model</label>
                <select className="mt-1 w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                  <option>Remote</option>
                  <option>Hybrid</option>
                  <option>On-site</option>
                </select>
              </div>
              <button type="button" className="w-full py-2 px-4 bg-gray-900 text-white rounded-lg hover:bg-gray-800">
                Save Preferences
              </button>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}
