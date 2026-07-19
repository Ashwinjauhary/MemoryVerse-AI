"use client";

import React, { useState } from "react";
import { UploadCloud, Link as LinkIcon, AlertCircle, FileType, CheckCircle2 } from "lucide-react";
import { supabase } from "../lib/supabase";
import { API_URL } from "@/lib/api";

export default function UploadUI({ userId, onUploadSuccess }: { userId: string; onUploadSuccess?: () => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [url, setUrl] = useState("");
  const [githubUsername, setGithubUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const [githubLoading, setGithubLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0];
      if (selectedFile.size > 10 * 1024 * 1024) {
        setError("File size exceeds 10MB limit. Please upload a smaller file.");
        setFile(null);
        e.target.value = '';
        return;
      }
      setError("");
      setFile(selectedFile);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file && !url) {
      setError("Please provide either a file or a URL link.");
      return;
    }
    
    setError("");
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    if (file) formData.append("file", file);
    if (url) formData.append("url", url);
    formData.append("user_id", userId);

    try {
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;

      const res = await fetch(`${API_URL}/api/documents/upload`, {
        method: "POST",
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData,
      });

      if (!res.ok) {
        let errorMessage = "Failed to upload document";
        try {
          const errData = await res.json();
          if (errData.detail) errorMessage = errData.detail;
        } catch (e) {
          // Keep default if JSON fails
        }
        throw new Error(errorMessage);
      }

      const data = await res.json();
      setResult(data);
      setFile(null);
      setUrl("");
      if (onUploadSuccess) onUploadSuccess();
    } catch (err: any) {
      setError(err.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleGithubSync = async () => {
    if (!githubUsername) {
      setError("Please enter a GitHub username.");
      return;
    }
    setError("");
    setGithubLoading(true);
    setResult(null);

    try {
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;

      const res = await fetch(`${API_URL}/api/documents/github`, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ username: githubUsername })
      });

      if (!res.ok) {
        let errorMessage = "Failed to sync GitHub repos";
        try {
          const errData = await res.json();
          if (errData.detail) errorMessage = errData.detail;
        } catch (e) {}
        throw new Error(errorMessage);
      }

      const data = await res.json();
      setResult(data);
      setGithubUsername("");
      if (onUploadSuccess) onUploadSuccess();
    } catch (err: any) {
      setError(err.message || "An error occurred during GitHub sync");
    } finally {
      setGithubLoading(false);
    }
  };

  return (
    <div className="relative w-full h-full flex flex-col">
      <div className={`flex-1 flex flex-col transition-all duration-500 ${result ? 'blur-md opacity-30 pointer-events-none' : ''}`}>
        <div className="mb-6 flex justify-between items-start">
          <div>
            <h2 className="text-xl font-bold text-white tracking-tight">Upload Document</h2>
            <p className="text-gray-400 text-sm mt-1">Add to your spatial archive</p>
          </div>
          <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center backdrop-blur-md border border-white/5">
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 4v16m8-8H4" />
            </svg>
          </div>
        </div>

        <form onSubmit={handleUpload} className="flex-1 flex flex-col space-y-5">
          
          {/* File Drop Zone (Inner Glass) */}
          <div className="relative group flex-1 min-h-[140px]">
            <div className="absolute inset-0 spatial-glass-inner flex flex-col items-center justify-center text-center cursor-pointer hover:bg-black/40 transition-colors">
              <svg className="w-8 h-8 text-white/50 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <p className="text-sm text-gray-300 font-medium">Drag & drop or click</p>
              <p className="text-xs text-gray-500 mt-1">PDF, PNG, JPG (10MB)</p>
              <input 
                type="file" 
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" 
                onChange={handleFileChange}
                accept=".pdf,image/png,image/jpeg"
              />
            </div>
          </div>

          {file && (
            <div className="flex items-center justify-between p-3 bg-blue-500/10 border border-blue-500/20 rounded-xl">
              <span className="text-sm text-blue-200 truncate">{file.name}</span>
              <button 
                type="button" 
                onClick={() => setFile(null)}
                className="text-blue-400 hover:text-blue-300 p-1"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </div>
          )}

          {/* URL Input */}
          <div>
            <input
              type="url"
              placeholder="Or paste a link (e.g. Medium)"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="w-full spatial-glass-inner px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:bg-black/50 transition-all text-sm"
            />
          </div>

          {error && <p className="text-red-400 text-xs">{error}</p>}

          <button
            type="submit"
            disabled={loading || githubLoading}
            className="w-full py-3.5 px-4 bg-white/10 hover:bg-white/20 backdrop-blur-xl border border-white/20 text-white font-medium rounded-xl transition-all focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed transform active:scale-95"
          >
            {loading ? "Processing Spatial Map..." : "Add to Archive"}
          </button>
          
          <div className="relative flex items-center justify-center py-2">
            <div className="border-t border-white/10 w-full"></div>
            <span className="bg-transparent px-3 text-xs text-white/40 absolute" style={{ background: '#0A0A0F' }}>OR</span>
          </div>

          <div className="flex flex-col gap-2">
            <input
              type="text"
              placeholder="Sync GitHub Username"
              value={githubUsername}
              onChange={(e) => setGithubUsername(e.target.value)}
              className="w-full spatial-glass-inner px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:bg-black/50 transition-all text-sm"
            />
            <button
              type="button"
              onClick={handleGithubSync}
              disabled={githubLoading || loading}
              className="w-full py-2.5 bg-zinc-800/80 hover:bg-zinc-700 border border-white/10 text-white text-sm font-medium rounded-xl transition-all disabled:opacity-50 flex items-center justify-center gap-2"
            >
              <svg viewBox="0 0 24 24" className="w-4 h-4 fill-current"><path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"></path></svg>
              {githubLoading ? "Syncing Top Repos..." : "Sync GitHub Repos"}
            </button>
          </div>
        </form>
      </div>

      {/* Success Result */}
      {result && (
        <div className="absolute inset-[-2rem] z-20 flex flex-col items-center justify-center p-6 animate-in text-center rounded-[28px] overflow-hidden">
          
          {/* Simple translucent background layer (blur is applied directly to the form behind it) */}
          <div className="absolute inset-0 bg-[#0A0A0F]/20"></div>
          
          {/* Content Layer */}
          <div className="relative z-10 flex flex-col items-center">
            <div className="w-12 h-12 rounded-full bg-green-500/20 border border-green-500/30 flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
            </div>
            <h3 className="text-white font-bold mb-2">Ingested Successfully</h3>
            <p className="text-sm text-gray-400 mb-6">AI has mapped this to your timeline.</p>
            <button 
              onClick={() => setResult(null)}
              className="px-6 py-2 bg-white/10 border border-white/10 rounded-full text-sm text-white hover:bg-white/20 transition-colors"
            >
              Upload Another
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
