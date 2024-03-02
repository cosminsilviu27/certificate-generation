import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { useApiUploadService } from '../hooks/useApiUploadService'; 
import { connect } from 'react-redux';
import { checkAuthenticated, load_user } from '../actions/auth';

function Secretary({ checkAuthenticated, load_user, user }) {
    const [filename, setFilename] = useState('');
    const [files, setFiles] = useState([]);
    const [status, setStatus] = useState('');
    const [subscription, setSubscription] = useState([]);
    const [selectedPlan, setSelectedPlan] = useState(null);
    const [selectedPlanType, setSelectedPlanType] = useState('');
    const { uploadFile, getFiles, getSubscriptionsTypes, downloadWithAxios, deleteWithAxios } = useApiUploadService(); 
    const history = useHistory();

    useEffect(() => {
        checkAuthenticated();
        load_user();
        fetchSubscriptionDetails();
        fetchFiles();
        console.log('Local Storage', localStorage);
    }, []);

    const fetchFiles = async () => {
        try {
            const filesList = await getFiles();
            setFiles(Array.isArray(filesList) ? filesList : []);
        } catch (error) {
            setStatus('Failed to load files');
            setFiles([]);
        }
    };

    const fetchSubscriptionDetails = async () => {
        try {
            const subscriptionList = await getSubscriptionsTypes();
            setSubscription(Array.isArray(subscriptionList) ? subscriptionList : []); 
        } catch (error) {
            setSubscription([]); 
        }
    };

    const handleFileUpload = async () => {
        if (!filename || !(filename instanceof File)) {
            setStatus('No file selected or invalid file');
            return;
        }
    
        const reader = new FileReader();
        reader.onloadend = async () => {
            try {
                await uploadFile(new Blob([reader.result], { type: 'application/pdf' }), filename.name);
                setStatus('File uploaded successfully');
                fetchFiles();
            } catch (error) {
                setStatus(`Error in file upload: ${error.message}`);
            }
        };
        reader.onerror = () => setStatus('Error reading the file');
        reader.readAsArrayBuffer(filename);
    };
    
    const handleFileChange = (event) => setFilename(event.target.files[0]);
    
    const handleFileDownload = async (fileId, title) => {
        try {
            await downloadWithAxios(fileId, title);
            fetchFiles();
        } catch (error) {
            setStatus('Error downloading file');
        }
    }; 
    
    const handleFileDelete = async (fileId, title) => {
        try {
            await deleteWithAxios(fileId, title);
            const updatedFiles = files.filter(file => file.id !== fileId);
            setFiles(updatedFiles)
        } catch (error) {
            setStatus('Error deleting file');
        }
    };

    const selectPlanHandler = (id, type) => {
        setSelectedPlan(id);
        setSelectedPlanType(type);
        history.push('/subscription', { selectedPlanId: id, selectedPlanType: type });
    };

    return (
        <div className="container-fluid">
            <h2 className="text-center alert alert-danger mt-2">Secretary Page</h2>
            {user && (
                <div className="alert alert-info">
                    Logged in as: {user.email} 
                </div>
            )}
            <div className="row">
                <div className="col-md-5">
                    <h2 className="alert alert-success">WORD Upload Section</h2>
                    <form>
                        <div className="form-group">
                            <label htmlFor="exampleFormControlFile1" className="float-left">Browse A WORD File To Upload</label>
                            <input type="file" multiple onChange={handleFileChange} className="form-control" />
                        </div>
                        <button type="button" onClick={handleFileUpload} className="btn btn-primary float-left mt-2">CONVERT</button>
                        <br/><br/><br/>
                        {status ? <h2>{status}</h2> : null}
                    </form>
                </div>
                <div className="col-md-7">
                    <h2 className="alert alert-success">List of Uploaded PDF Files</h2>
                    <table className="table table-bordered mt-4">
                        <thead>
                            <tr>
                                <th scope="col">File Title</th>
                                <th scope="col">Download</th>
                            </tr>
                        </thead>
                        <tbody>
                            {files.map(file => (
                                <tr key={file.id}>
                                    <td>{file.word_file_name}</td>
                                    <td>
                                        <button onClick={() => handleFileDownload(file.id, file.word_file_name)} className="btn btn-success" style={{ marginRight: '20px' }}>Download</button>
                                        <button onClick={() => handleFileDelete(file.id, file.word_file_name)} class="btn btn-danger">Delete</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
            <div className="subscription-plans mt-4">
            <h2 className="text-center alert alert-info">Subscription Plans</h2>
            <div className="row">
                {Array.isArray(subscription) && subscription.map(subscription_type => (
                    <div key={subscription_type.id} className="col-md-4 mb-4">
                        <div 
                            className={`card text-center ${selectedPlan === subscription_type.id ? 'border-primary' : ''}`}
                            onClick={() => selectPlanHandler(subscription_type.id, subscription_type.subscription_type)}
                            style={{ cursor: 'pointer' }}
                        >
                            <div className="card-header">{subscription_type.subscription_type}</div>
                            <div className="card-body">
                                <h5 className="card-title">{subscription_type.price}</h5>
                                <p className="card-text">{subscription_type.features}</p>
                                <p className="card-text">{subscription_type.available}</p>
                                <p className="card-text">{subscription_type.cancel}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
        </div>
    );
}

const mapStateToProps = state => {
    console.log(state); 
    return {
        user: state.auth.user 
    };
}

export default connect(mapStateToProps, { checkAuthenticated, load_user })(Secretary);

