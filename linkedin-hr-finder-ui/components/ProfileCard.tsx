'use client'

import { useState } from 'react'
import { ExternalLink, Copy, Check, MapPin, Briefcase, MessageSquare, Send } from 'lucide-react'
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
      setTimeout(() => setCopiedConnection(false), 2000)
    }
  }

  const handleCopyFollowup = async () => {
    const success = await copyToClipboard(contact.follow_up_message)
    if (success) {
      setCopiedFollowup(true)
      setTimeout(() => setCopiedFollowup(false), 2000)
    }
  }

  const handleOpenLinkedIn = () => {
    window.open(contact.profile_url, '_blank', 'noopener,noreferrer')
  }

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-linkedin-500 to-linkedin-600 p-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h3 className="text-xl font-bold text-white mb-1">{contact.name}</h3>
            <div className="flex items-center text-linkedin-50 text-sm mb-2">
              <Briefcase className="h-4 w-4 mr-1" />
              {contact.title}
            </div>
            <div className="flex items-center text-linkedin-100 text-xs">
              <MapPin className="h-3 w-3 mr-1" />
              {contact.location}
            </div>
          </div>
          <button
            onClick={handleOpenLinkedIn}
            className="bg-white text-linkedin-600 hover:bg-linkedin-50 rounded-lg px-4 py-2 text-sm font-medium flex items-center transition-colors"
          >
            <ExternalLink className="h-4 w-4 mr-1" />
            View Profile
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="p-5 space-y-4">
        {/* Connection Request */}
        <div className="border border-gray-200 rounded-lg p-4 bg-gray-50">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center">
              <MessageSquare className="h-4 w-4 text-linkedin-600 mr-2" />
              <span className="text-sm font-semibold text-gray-700">Connection Request</span>
            </div>
            <span className="text-xs text-gray-500">{contact.char_count_connection} chars</span>
          </div>

          <p className="text-sm text-gray-700 leading-relaxed mb-3 whitespace-pre-wrap">
            {contact.connection_request}
          </p>

          <div className="flex gap-2">
            <button
              onClick={handleCopyConnection}
              className={cn(
                "flex-1 flex items-center justify-center px-4 py-2 rounded-md text-sm font-medium transition-colors",
                copiedConnection
                  ? "bg-green-500 text-white"
                  : "bg-linkedin-500 hover:bg-linkedin-600 text-white"
              )}
            >
              {copiedConnection ? (
                <>
                  <Check className="h-4 w-4 mr-1" />
                  Copied!
                </>
              ) : (
                <>
                  <Copy className="h-4 w-4 mr-1" />
                  Copy Message
                </>
              )}
            </button>
            <button
              onClick={handleOpenLinkedIn}
              className="flex-1 flex items-center justify-center px-4 py-2 rounded-md text-sm font-medium bg-gray-200 hover:bg-gray-300 text-gray-700 transition-colors"
            >
              <Send className="h-4 w-4 mr-1" />
              Send on LinkedIn
            </button>
          </div>
        </div>

        {/* Follow-up Message */}
        <div className="border border-gray-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center">
              <MessageSquare className="h-4 w-4 text-linkedin-600 mr-2" />
              <span className="text-sm font-semibold text-gray-700">Follow-up Message</span>
            </div>
            <span className="text-xs text-gray-500">{contact.char_count_followup} chars</span>
          </div>

          <div className="max-h-48 overflow-y-auto">
            <p className="text-sm text-gray-700 leading-relaxed mb-3 whitespace-pre-wrap">
              {contact.follow_up_message}
            </p>
          </div>

          <button
            onClick={handleCopyFollowup}
            className={cn(
              "w-full flex items-center justify-center px-4 py-2 rounded-md text-sm font-medium transition-colors",
              copiedFollowup
                ? "bg-green-500 text-white"
                : "bg-gray-100 hover:bg-gray-200 text-gray-700"
            )}
          >
            {copiedFollowup ? (
              <>
                <Check className="h-4 w-4 mr-1" />
                Copied!
              </>
            ) : (
              <>
                <Copy className="h-4 w-4 mr-1" />
                Copy Follow-up
              </>
            )}
          </button>
        </div>

        {/* Metadata */}
        <div className="flex items-center justify-between text-xs text-gray-500 pt-2 border-t">
          <span>Generated by {contact.ai_provider === 'openai' ? 'GPT-4' : 'Claude'}</span>
          <span>{new Date(contact.generated_at).toLocaleTimeString()}</span>
        </div>
      </div>
    </div>
  )
}
