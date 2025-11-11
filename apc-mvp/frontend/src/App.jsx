import React, {useState} from 'react'
import Chat from './components/Chat'


export default function App(){
return (
<div className="min-h-screen bg-gray-50 p-4">
<div className="max-w-2xl mx-auto bg-white shadow p-4 rounded-lg">
<h1 className="text-xl font-bold mb-4">AI Productivity Coach</h1>
<Chat />
</div>
</div>
)
}