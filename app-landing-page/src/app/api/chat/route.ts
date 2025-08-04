import { NextRequest, NextResponse } from 'next/server';
/* OpenAI integration disabled */
// import { OpenAI } from 'openai';
// const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function POST(req: NextRequest) {
  // OpenAI integration is disabled. Return a stub response.
  return NextResponse.json({
    reply: "OpenAI integration is currently disabled. No response generated."
  });
}