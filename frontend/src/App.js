import React, { useState, useEffect } from 'react';
import SpeechToText from './components/SpeechToText';
import SubmitRequest from './components/SubmitRequest';
import './App.css';
import logo from './logo.png'; // Import the logo
import axios from 'axios';

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
            const filtered = requests.filter(req => req.fields.department === activeTab);
            setFilteredRequests(filtered);
        }
    }, [activeTab, requests]);

    const renderContent = () => {
        if (activeTab === 'home') {
            return (
                <>
                    <img src={logo} alt="Talkability Logo" className="app-logo"/>
                    <SpeechToText setTranscribedText={setTranscribedText}/>
                    <SubmitRequest
                        text={transcribedText}
                        setText={setTranscribedText}
                        refreshRequests={() => {
                            // Re-fetch requests after submission
                            axios.get('http://127.0.0.1:5000/get-requests').then((response) => {
                                setRequests(response.data);
                            });
                        }}
                    />
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
                                    <strong>Name:</strong> {req.fields.name || 'N/A'}
                                </p>
                                <p>
                                    <strong>ID Number:</strong> {req.fields.id_number || 'N/A'}
                                </p>
                                <p>
                                    <strong>Contact Number:</strong> {req.fields.contact_number || 'N/A'}
                                </p>
                                <p>
                                    <strong>Request Type:</strong> {req.fields.type_of_request || 'N/A'}
                                </p>
                                <p>
                                    <strong>Details:</strong> {req.fields.specific_request_details}
                                </p>
                                <p>
                                    <strong>Urgency:</strong> {req.fields.urgency_level}
                                </p>
                                <p>
                                    <strong>Full Request:</strong> {req.formatted_request}
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
            <div className="sidebar">
                <ul className="sidebar-menu">
                    <li className={activeTab === 'home' ? 'active' : ''} onClick={() => setActiveTab('home')}>
                        Home
                    </li>
                    <li
                        className={activeTab === 'Technical Support' ? 'active' : ''}
                        onClick={() => setActiveTab('Technical Support')}
                    >
                        Technical Support
                    </li>
                    <li className={activeTab === 'Billing' ? 'active' : ''} onClick={() => setActiveTab('Billing')}>
                        Billing
                    </li>
                    <li className={activeTab === 'Sales' ? 'active' : ''} onClick={() => setActiveTab('Sales')}>
                        Sales
                    </li>
                    <li className={activeTab === 'Insurance' ? 'active' : ''} onClick={() => setActiveTab('Insurance')}>
                        Insurance
                    </li>
                    <li className={activeTab === 'General' ? 'active' : ''} onClick={() => setActiveTab('General')}>
                        General
                    </li>
                </ul>
            </div>
            <div className="content">{renderContent()}</div>
        </div>
    );
};

export default App;
