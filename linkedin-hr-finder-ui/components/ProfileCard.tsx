'use client'

import { useState } from 'react'
import { ExternalLink, Copy, Check, MapPin, Briefcase, MessageSquare, Send, Sparkles } from 'lucide-react'
import type { HRContact } from '@/lib/types'
import { copyToClipboard, cn } from '@/lib/utils'

interface ProfileCardProps {
  contact: HRContact
}

export default function ProfileCard({ contact }: ProfileCardProps) {
  const [copiedConnection, setCopiedConnection] = useState(false)
  const [copiedFollowup, setCopiedFollowup] = useState(false)

  const handleCopyConnection = async () => {
    const success = await copyToClipboard(contact.connection_request)
    if (success) {
      setCopiedConnection(true)
      setTimeout(() => setCopiedConnection(false), 2500)
    }
  }

  const handleCopyFollowup = async () => {
    const success = await copyToClipboard(contact.follow_up_message)
    if (success) {
      setCopiedFollowup(true)
      setTimeout(() => setCopiedFollowup(false), 2500)
    }
  }

  const handleOpenLinkedIn = () => {
    window.open(contact.profile_url, '_blank', 'noopener,noreferrer')
  }

  return (
    <div className="stripe-card group animate-scale-in hover:scale-[1.01] hover:shadow-brand-lg transition-all duration-300 border border-neutral-100">
      {/* Header - Professional Style */}
      <div className="border-b border-neutral-100 p-6 bg-gradient-to-br from-neutral-50 to-white">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2.5 mb-2.5">
              <h3 className="text-xl font-bold text-neutral-900 truncate">{contact.name}</h3>
              <span className="stripe-badge bg-gradient-to-br from-linkedin-100 to-linkedin-50 text-linkedin-700 text-xs border border-linkedin-300 flex-shrink-0 font-bold shadow-sm">
                HR
              </span>
            </div>
            <div className="flex items-center text-neutral-700 text-sm mb-2 font-medium">
              <div className="bg-neutral-200 p-1 rounded mr-2">
                <Briefcase className="h-3.5 w-3.5 text-neutral-600" />
              </div>
              <span className="truncate">{contact.title}</span>
            </div>
            <div className="flex items-center text-neutral-600 text-xs font-medium">
              <div className="bg-neutral-200 p-1 rounded mr-2">
                <MapPin className="h-3 w-3 text-neutral-500" />
              </div>
              <span className="truncate">{contact.location}</span>
            </div>
          </div>
          <button
            onClick={handleOpenLinkedIn}
            className="stripe-button-secondary px-4 py-2.5 text-xs flex-shrink-0 font-bold hover:border-linkedin-500 hover:text-linkedin-700 hover:bg-linkedin-50 transition-all"
          >
            <ExternalLink className="h-4 w-4 mr-1.5" />
            <span>View</span>
          </button>
        </div>
      </div>

      {/* Messages Section */}
      <div className="p-6 space-y-5">
        {/* Connection Request */}
        <div className="relative group/msg">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-linkedin-100 to-linkedin-200 p-2 rounded-xl shadow-linkedin-sm">
                <MessageSquare className="h-4 w-4 text-linkedin-700" />
              </div>
              <span className="text-sm font-bold text-neutral-900">Connection Request</span>
            </div>
            <span className="stripe-badge bg-neutral-100 text-neutral-700 border border-neutral-300 text-xs font-semibold">
              {contact.char_count_connection} chars
            </span>
          </div>

          <div className="bg-gradient-to-br from-neutral-50 via-white to-brand-50/20 border-2 border-neutral-200 rounded-xl p-5 mb-4 group-hover/msg:border-brand-300 group-hover/msg:shadow-brand transition-all">
            <p className="text-sm text-neutral-800 leading-relaxed whitespace-pre-wrap font-medium">
              {contact.connection_request}
            </p>
          </div>

          <div className="flex gap-3">
            <button
              onClick={handleCopyConnection}
              className={cn(
                "flex-1 flex items-center justify-center px-5 py-3 rounded-xl text-sm font-bold transition-all duration-200 shadow-lg",
                copiedConnection
                  ? "bg-success-500 text-white shadow-success-500/30 scale-[0.98]"
                  : "bg-gradient-to-r from-linkedin-500 to-linkedin-600 hover:from-linkedin-600 hover:to-linkedin-700 text-white hover:shadow-linkedin hover:scale-[1.02]"
              )}
            >
              {copiedConnection ? (
                <>
                  <Check className="h-4 w-4 mr-2" />
                  Copied!
                </>
              ) : (
                <>
                  <Copy className="h-4 w-4 mr-2" />
                  Copy Message
                </>
              )}
            </button>
            <button
              onClick={handleOpenLinkedIn}
              className="flex-1 stripe-button-secondary py-3 flex items-center justify-center font-bold hover:bg-neutral-100 hover:scale-[1.02] transition-all"
            >
              <Send className="h-4 w-4 mr-2" />
              Send on LinkedIn
            </button>
          </div>
        </div>

        {/* Divider */}
        <div className="relative py-2">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t-2 border-dashed border-neutral-300"></div>
          </div>
          <div className="relative flex justify-center">
            <span className="bg-white px-4 py-1 text-xs text-neutral-600 font-bold uppercase tracking-wider border border-neutral-300 rounded-full shadow-sm">
              Follow-up
            </span>
          </div>
        </div>

        {/* Follow-up Message */}
        <div className="relative group/followup">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-brand-100 to-brand-200 p-2 rounded-xl shadow-brand-sm">
                <Sparkles className="h-4 w-4 text-brand-700" />
              </div>
              <span className="text-sm font-bold text-neutral-900">Follow-up Message</span>
            </div>
            <span className="stripe-badge bg-brand-50 text-brand-700 border border-brand-300 text-xs font-semibold">
              {contact.char_count_followup} chars
            </span>
          </div>

          <div className="bg-gradient-to-br from-brand-50/30 via-white to-accent-50/20 border-2 border-brand-200 rounded-xl p-5 mb-4 max-h-56 overflow-y-auto group-hover/followup:border-brand-400 group-hover/followup:shadow-brand-lg transition-all custom-scrollbar">
            <p className="text-sm text-neutral-800 leading-relaxed whitespace-pre-wrap font-medium">
              {contact.follow_up_message}
            </p>
          </div>

          <button
            onClick={handleCopyFollowup}
            className={cn(
              "w-full flex items-center justify-center px-5 py-3 rounded-xl text-sm font-bold transition-all duration-200 shadow-lg",
              copiedFollowup
                ? "bg-success-500 text-white shadow-success-500/30 scale-[0.98]"
                : "bg-gradient-to-r from-brand-500 to-accent-500 hover:from-brand-600 hover:to-accent-600 text-white hover:shadow-brand-lg hover:scale-[1.02]"
            )}
          >
            {copiedFollowup ? (
              <>
                <Check className="h-4 w-4 mr-2" />
                Copied!
              </>
            ) : (
              <>
                <Copy className="h-4 w-4 mr-2" />
                Copy Follow-up
              </>
            )}
          </button>
        </div>

        {/* Metadata Footer */}
        <div className="flex items-center justify-between text-xs pt-5 border-t-2 border-neutral-200 mt-2">
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-success-500 animate-pulse shadow-lg shadow-success-500/50"></div>
            <span className="text-neutral-600 font-medium">Generated by</span>
            <span className="font-bold text-brand-700 bg-brand-50 px-2 py-0.5 rounded border border-brand-200">
              {contact.ai_provider === 'openai' ? 'GPT-4' : 'Claude AI'}
            </span>
          </div>
          <span className="text-neutral-500 font-semibold bg-neutral-100 px-2 py-0.5 rounded">
            {new Date(contact.generated_at).toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit'
            })}
          </span>
        </div>
      </div>
    </div>
  )
}
