import React from "react";
import './Modal.css';

const Modal = ({ response, closeModal }) => {
    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <h3>Data Summary</h3>
                <p>The data we got from the record is:</p>
                <div className="response-summary">
                    <p className="field"><strong>Name:</strong> {response.name || 'N/A'}</p>
                    <p className="field"><strong>ID Number:</strong> {response.id_number || 'N/A'}</p>
                    <p className="field"><strong>Department:</strong> {response.department || 'N/A'}</p>
                    <p className="field"><strong>Urgency Level:</strong> {response.urgency_level || 'N/A'}</p>
                </div>
                <p>You can view the full request details in the tab <strong>{response.department || 'N/A'}</strong>.</p>
                <button onClick={closeModal}>Close</button>
            </div>
        </div>
    );
};

export default Modal;