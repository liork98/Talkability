import React, { useState } from 'react';
import { speechToText } from '../api';
import './SpeechToText.css';

const SpeechToText = ({ setTranscribedText }) => {
    const [audioFile, setAudioFile] = useState(null);

    const handleFileChange = (e) => {
        setAudioFile(e.target.files[0]);
    };

    const handleSubmit = async () => {
        if (!audioFile) {
            alert('Please upload an audio file.');
            return;
        }

        try {
            const result = await speechToText(audioFile);
            setTranscribedText(result.text);
        } catch (error) {
            alert('Error processing speech-to-text.');
        }
    };

    return (
        <div className="speech-container">
            <h2>Speech to Text</h2>
            <input type="file" accept="audio/*" onChange={handleFileChange} />
            <button onClick={handleSubmit}>Upload and Transcribe</button>
        </div>
    );
};

export default SpeechToText;
