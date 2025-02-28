import React, { useState } from 'react';
import { speechToText, submitRequest } from '../api';
import './SpeechToText.css';
import Modal from './Modal.jsx';
import Spinner from './Spinner'; // Import Spinner component

const SpeechToText = ({ setTranscribedText }) => {
    const [audioFile, setAudioFile] = useState(null);
    const [response, setResponse] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isLoading, setIsLoading] = useState(false); // New state to track loading

    const handleFileChange = (e) => {
        setAudioFile(e.target.files[0]);
    };

    const handleSubmit = async () => {
        if (!audioFile) {
            alert('Please upload an audio file.');
            return;
        }
        setIsLoading(true); // Set loading to true when the process starts
        try {
            const result = await speechToText(audioFile);
            console.log("QQQQQQQQQQQQQQQQQQQQ ", result)
            setTranscribedText(result.text);
            const resultt = await submitRequest(result.text);
            console.log("HIHIHHIHL ", resultt);
            setResponse(resultt);
            setIsModalOpen(true); // Open modal after receiving the response
        } catch (error) {
            alert('Error processing speech-to-text.');
        } finally {
            setIsLoading(false); // Reset loading once the process is complete
        }
    };

    const closeModal = () => {
        setIsModalOpen(false); // Close the modal
    };

    return (
        <div className="speech-container">
            <h2>Speech to Text</h2>
            <input type="file" accept="audio/*" onChange={handleFileChange} />
            <button onClick={handleSubmit} disabled={isLoading}>
                {isLoading ? (
                    <Spinner /> // Use the Spinner component while loading
                ) : (
                    "Upload and Transcribe"
                )}
            </button>
            {isModalOpen && response && <Modal response={response} closeModal={closeModal} />}
        </div>
    );
};

export default SpeechToText;