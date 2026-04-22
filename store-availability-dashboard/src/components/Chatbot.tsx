import React, { useState, useRef, useEffect } from "react";
import api from "../api/client";
import type { ChatResponse } from "../types";
import "./Chatbot.css";

interface Props {
    storeId: string;
    fromDate: string;
    toDate: string;
}

type Message = {
    role: "user" | "bot";
    content: string;
};

const Chatbot: React.FC<Props> = ({ storeId, fromDate, toDate }) => {
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState<Message[]>([
        { role: "bot", content: "Hola 👋 Pregúntame lo que quieras sobre los CSV." }
    ]);
    const [loading, setLoading] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    const ask = async () => {
        if (!question.trim()) return;

        const userMessage: Message = { role: "user", content: question };
        setMessages((prev) => [...prev, userMessage]);
        setQuestion("");
        setLoading(true);

        const payload = {
            question,
            store_id: storeId || undefined,
            from_date: fromDate || undefined,
            to_date: toDate || undefined
        };

        try {
            const res = await api.post<ChatResponse>("/api/chatbot", payload);
            const botMessage: Message = { role: "bot", content: res.data.answer };
            setMessages((prev) => [...prev, botMessage]);
        } catch {
            setMessages((prev) => [
                ...prev,
                { role: "bot", content: "Ocurrió un error consultando el chatbot." }
            ]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
    }, [messages, loading]);

    return (
        <div className="card chatbot-card">
            <div className="chatbot-header">
                <div className="chatbot-title">Chatbot</div>
                <div className="chatbot-status">Online</div>
            </div>

            <div className="chat-window" ref={scrollRef}>
                {messages.map((m, i) => (
                    <div key={i} className={`message ${m.role}`}>
                        <div className="avatar">{m.role === "user" ? "Tú" : "AI"}</div>
                        <div className="bubble">{m.content}</div>
                    </div>
                ))}
                {loading && <div className="typing">Escribiendo...</div>}
            </div>

            <div className="input-row">
                <input
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Escribe tu pregunta..."
                    onKeyDown={(e) => e.key === "Enter" && ask()}
                />
                <button onClick={ask}>Enviar</button>
            </div>
        </div>
    );
};

export default Chatbot;