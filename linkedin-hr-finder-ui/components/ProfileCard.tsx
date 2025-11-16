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
    <div className="stripe-card group animate-scale-in hover:scale-[1.01] transition-all duration-300">
      {/* Header - Stripe Style */}
      <div className="border-b border-gray-100 p-5">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-2">
              <h3 className="text-lg font-semibold text-gray-900 truncate">{contact.name}</h3>
              <span className="stripe-badge bg-linkedin-50 text-linkedin-700 text-xs border border-linkedin-200 flex-shrink-0">
                HR
              </span>
            </div>
            <div className="flex items-center text-gray-600 text-sm mb-1.5">
              <Briefcase className="h-3.5 w-3.5 mr-1.5 text-gray-400" />
              <span className="truncate">{contact.title}</span>
            </div>
            <div className="flex items-center text-gray-500 text-xs">
              <MapPin className="h-3 w-3 mr-1.5 text-gray-400" />
              <span className="truncate">{contact.location}</span>
            </div>
          </div>
          <button
            onClick={handleOpenLinkedIn}
            className="stripe-button-secondary px-4 py-2 text-xs flex-shrink-0 hover:border-linkedin-300 hover:text-linkedin-600"
          >
            <ExternalLink className="h-3.5 w-3.5 mr-1.5" />
            <span>View</span>
          </button>
        </div>
      </div>

      {/* Messages Section */}
      <div className="p-6 space-y-5">
        {/* Connection Request */}
        <div className="relative group/msg">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <div className="bg-linkedin-100 p-1.5 rounded-lg">
                <MessageSquare className="h-4 w-4 text-linkedin-600" />
              </div>
              <span className="text-sm font-semibold text-gray-900">Connection Request</span>
            </div>
            <span className="stripe-badge bg-gray-50 text-gray-600 border border-gray-200 text-xs">
              {contact.char_count_connection} chars
            </span>
          </div>

          <div className="bg-gradient-to-br from-gray-50 to-white border border-gray-200 rounded-lg p-4 mb-3 group-hover/msg:border-gray-300 transition-colors">
            <p className="text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">
              {contact.connection_request}
            </p>
          </div>

          <div className="flex gap-2.5">
            <button
              onClick={handleCopyConnection}
              className={cn(
                "flex-1 flex items-center justify-center px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 shadow-stripe",
                copiedConnection
                  ? "bg-success-500 text-white shadow-success-500/20"
                  : "bg-linkedin-500 hover:bg-linkedin-600 text-white hover:shadow-linkedin-500/30"
              )}
            >
              {copiedConnection ? (
                <>
                  <Check className="h-4 w-4 mr-1.5" />
                  Copied!
                </>
              ) : (
                <>
                  <Copy className="h-4 w-4 mr-1.5" />
                  Copy Message
                </>
              )}
            </button>
            <button
              onClick={handleOpenLinkedIn}
              className="flex-1 stripe-button-secondary py-2.5 flex items-center justify-center"
            >
              <Send className="h-4 w-4 mr-1.5" />
              Send on LinkedIn
            </button>
          </div>
        </div>

        {/* Divider */}
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-200"></div>
          </div>
          <div className="relative flex justify-center">
            <span className="bg-white px-3 text-xs text-gray-400 font-medium">Follow-up</span>
          </div>
        </div>

        {/* Follow-up Message */}
        <div className="relative group/followup">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <div className="bg-stripe-100 p-1.5 rounded-lg">
                <Sparkles className="h-4 w-4 text-stripe-600" />
              </div>
              <span className="text-sm font-semibold text-gray-900">Follow-up Message</span>
            </div>
            <span className="stripe-badge bg-stripe-50 text-stripe-600 border border-stripe-200 text-xs">
              {contact.char_count_followup} chars
            </span>
          </div>

          <div className="bg-gradient-to-br from-stripe-50 to-white border border-stripe-200 rounded-lg p-4 mb-3 max-h-52 overflow-y-auto group-hover/followup:border-stripe-300 transition-colors custom-scrollbar">
            <p className="text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">
              {contact.follow_up_message}
            </p>
          </div>

          <button
            onClick={handleCopyFollowup}
            className={cn(
              "w-full flex items-center justify-center px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 shadow-stripe",
              copiedFollowup
                ? "bg-success-500 text-white shadow-success-500/20"
                : "bg-stripe-100 hover:bg-stripe-200 text-stripe-700 border border-stripe-200 hover:border-stripe-300"
            )}
          >
            {copiedFollowup ? (
              <>
                <Check className="h-4 w-4 mr-1.5" />
                Copied!
              </>
            ) : (
              <>
                <Copy className="h-4 w-4 mr-1.5" />
                Copy Follow-up
              </>
            )}
          </button>
        </div>

        {/* Metadata Footer */}
        <div className="flex items-center justify-between text-xs pt-4 border-t border-gray-100">
          <div className="flex items-center gap-1.5">
            <div className="h-1.5 w-1.5 rounded-full bg-success-500 animate-pulse"></div>
            <span className="text-gray-500">Generated by</span>
            <span className="font-semibold text-gray-700">
              {contact.ai_provider === 'openai' ? 'GPT-4' : 'Claude AI'}
            </span>
          </div>
          <span className="text-gray-400">
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
