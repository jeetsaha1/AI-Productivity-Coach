import React from 'react'


export default function ChatBubble({text, from}){
const isUser = from === 'user'
return (
<div className={`my-2 flex ${isUser ? 'justify-end' : 'justify-start'}`}>
<div className={`${isUser ? 'bg-blue-500 text-white' : 'bg-gray-200 text-black'} p-3 rounded-lg max-w-[80%]`}>{text}</div>
</div>
)
}