import React, { useState, useEffect } from 'react';
import axios from 'axios';

import styled from 'styled-components';

const ChatWindow = styled.div`
  width: 400px;
  height: 500px;  
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
`;

const ChatLog = styled.div`
  height: 90%;
  overflow-y: scroll;
  padding: 10px;
`;

const ChatInput = styled.textarea`
  width: 100%; 
  height: 10%;
  padding: 10px;
  box-sizing: border-box;
  border: none;
  border-top: 1px solid #ddd;
  resize: none;
`;

function Chatbot() {

  const [chatLog, setChatLog] = useState([{
    user: 'bot', 
    message: 'Hi there! I\'m a Chatbot, ask me anything.'
  }]);
const [idleTimer,setIdleTimer]=useState(null);
useEffect(()=>{
  setIdleTimer(setTimeout(handleIdle,60000));
  return ()=>{
    clearTimeout(idleTimer);
  }
},[]);


  const [input,setInput]=useState("")
  const handleKeyDown = async (e) => {
    if (e.keyCode === 13) {
      handleSubmit(e);
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    clearTimeout(idleTimer)
    setIdleTimer(setTimeout(handleIdle,120000))
    const userMessage = input
    setChatLog([...chatLog, { user: 'human', message: userMessage }]);
    const nextChatLog= [...chatLog, { user: 'human', message: userMessage }]
    setInput("")

    try {
      const response = await axios.post('http://localhost:5000/data', {
        data:userMessage
      });
      setChatLog([...nextChatLog, { user: 'bot', message: response.data.message }]); 


    } catch(err) {
      setChatLog([...chatLog, { user: 'bot', message: 'Sorry, something went wrong.' }]);
    }
  }
  const handleIdle=async()=>{
    const response=await axios.get('http://localhost:5000/');
    setChatLog([...chatLog, { user: 'bot', message: response.data.message }]);

  }
  

  return (
    <ChatWindow>
      <ChatLog>
        {chatLog.map((msg, index) => (
          <div key={index}>
            <b>{msg.user}:</b> {msg.message}
          </div>
        ))}
      </ChatLog>

      <form 
      style={{
        width:"100%",
        flexDirection:"column"
      }}>
        <ChatInput placeholder="Ask me anything..." style={{
            resize:"none",
        }}
        value={input}
        onChange={(e)=>setInput(e.target.value)}
        onKeyDown={handleKeyDown} 
        />
      </form>
    </ChatWindow>
  );
}

export default Chatbot;
