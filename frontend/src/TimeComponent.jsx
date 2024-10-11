import React, { useEffect, useState } from "react";
let ws;
const TimeDisplay = () => {
  const [timeData, setTimeData] = useState({
    time: "",
    connectionId: "",
    message: "",
  });
  const [message, setMessage] = useState("");
  

  useEffect(() => {
    const wsUrl = import.meta.env.VITE_REACT_APP_WS_URL;
     ws = new WebSocket(`${wsUrl}/ws`);

    ws.onopen = () => {
      ws.send("Connected");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data); // Parse the JSON data
      setTimeData({
        time: data.time,
        connectionId: data.connection_id,
        message: data.message,
      });
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div className="flex justify-center items-center min-h-fit">
      <div className="flex-1">
        <p className="text-gray-400">
          Time: {timeData.time || "Connecting..."}
        </p>
        <p className="text-gray-400">Connection ID: {timeData.connectionId.slice(0,8)}</p>
        <p className="text-gray-400">Server Message: {timeData.message}</p>
      </div>

      {/* <div className="mt-4">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Enter message"
            className="border p-2"
          />
          <button
            onClick={sendMessage}
            className="ml-2 p-2 bg-blue-500 text-white"
          >
            Send Message
          </button>
        </div> */}
    </div>
  );
};

export default TimeDisplay;
