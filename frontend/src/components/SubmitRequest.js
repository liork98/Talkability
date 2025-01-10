import React, { useState } from 'react';
import { submitRequest } from '../api';
import './SubmitRequest.css';

const SubmitRequest = ({ text, setText, refreshRequests }) => {
    const [response, setResponse] = useState(null);

    const handleSubmit = async () => {
        if (!text) {
            alert('Please enter your request text.');
            return;
        }

        try {
            const result = await submitRequest(text);
            setResponse(result);
            setText(''); // Clear the textarea
            refreshRequests(); // Reload requests
        } catch (error) {
            alert('Error submitting request.');
        }
    };

    const renderResponse = () => {
        if (!response) return null;

        const { fields, formatted_request } = response;

        return (
            <div className="response-container">
                <h3>Request Details</h3>
                <div className="response-fields">
                    <p><strong>Name:</strong> {fields.name || 'N/A'}</p>
                    <p><strong>ID Number:</strong> {fields.id_number || 'N/A'}</p>
                    <p><strong>Contact Number:</strong> {fields.contact_number || 'N/A'}</p>
                    <p><strong>Contact Preference:</strong> {fields.contact_preference || 'N/A'}</p>
                    <p><strong>Department:</strong> {fields.department || 'N/A'}</p>
                    <p><strong>Type of Request:</strong> {fields.type_of_request || 'N/A'}</p>
                    <p><strong>Specific Details:</strong> {fields.specific_request_details || 'N/A'}</p>
                    <p><strong>Urgency Level:</strong> {fields.urgency_level || 'N/A'}</p>
                </div>
                <h4>Formatted Request</h4>
                <p className="formatted-request">{formatted_request}</p>
            </div>
        );
    };

    return (
        <div className="request-container">
            <h2>Submit Request</h2>
            <textarea
                placeholder="Enter your request here..."
                value={text}
                onChange={(e) => setText(e.target.value)}
            ></textarea>
            <button onClick={handleSubmit}>Submit Request</button>
            {renderResponse()}
        </div>
    );
};

export default SubmitRequest;
