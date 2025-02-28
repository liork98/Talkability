// App.js
import React, { useState, useEffect } from 'react';
import SpeechToText from './components/SpeechToText';
import SubmitRequest from './components/SubmitRequest';
import './App.css';
import logo from './logo.png'; // Import the logo
import axios from 'axios';
import Sidebar from './components/Sidebar'; // Import the Sidebar component

const App = () => {
    const [transcribedText, setTranscribedText] = useState('');
    const [activeTab, setActiveTab] = useState('home'); // Tracks the active tab
    const [requests, setRequests] = useState([]); // Stores all requests
    const [filteredRequests, setFilteredRequests] = useState([]); // Stores requests filtered by department

    // Fetch all requests from the backend
    useEffect(() => {
        const fetchRequests = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/get-requests');
                setRequests(response.data);
            } catch (error) {
                console.error('Error fetching requests:', error);
            }
        };

        fetchRequests();
    }, []);

    // Filter requests when the active tab changes
    useEffect(() => {
        if (activeTab === 'home') {
            setFilteredRequests([]);
        } else {
            const filtered = requests.filter(req => req.department === activeTab);
            setFilteredRequests(filtered);
        }
    }, [activeTab, requests]);

    const renderContent = () => {
        if (activeTab === 'home') {
            return (
                <>
                    <img src={logo} alt="Talkability Logo" className="app-logo"/>
                    <SpeechToText setTranscribedText={setTranscribedText}/>
                </>
            );
        } else {
            return (
                <div className="requests-list">
                    <h2>{activeTab} Requests</h2>
                    {filteredRequests.length > 0 ? (
                        filteredRequests.map((req, index) => (
                            <div key={index} className="request-item">
                                <p>
                                    <strong>Name:</strong> {req.name || 'N/A'}
                                </p>
                                <p>
                                    <strong>ID Number:</strong> {req.id_number || 'N/A'}
                                </p>
                                <p>
                                    <strong>Contact Number:</strong> {req.contact_number || 'N/A'}
                                </p>
                                <p>
                                    <strong>Request Type:</strong> {req.type_of_request || 'N/A'}
                                </p>
                                {/*<p>*/}
                                {/*    <strong>Details:</strong> {req.fields.specific_request_details}*/}
                                {/*</p>*/}
                                <p>
                                    <strong>Urgency:</strong> {req.urgency_level}
                                </p>
                                <p>
                                    <strong>Full Request:</strong> {req.text}
                                </p>
                            </div>
                        ))
                    ) : (
                        <p>No requests for this department.</p>
                    )}
                </div>
            );
        }
    };

    return (
        <div className="app-container">
            <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} /> {/* Use the Sidebar component */}
            <div className="content">{renderContent()}</div>
        </div>
    );
};

export default App;