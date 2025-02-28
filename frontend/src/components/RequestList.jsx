import React from 'react';
import './RequestList.css';

const RequestList = ({ requests }) => {
    return (
        <div className="request-list">
            <h3>Requests</h3>
            {requests.length === 0 ? (
                <p className="no-requests">No requests for this department.</p>
            ) : (
                <div className="requests-container">
                    {requests.map((request) => (
                        <div key={request.id} className="request-card">
                            <p>
                                <strong>Department:</strong> {request.department}
                            </p>
                            <p>
                                <strong>Details:</strong> {request.details}
                            </p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default RequestList;
