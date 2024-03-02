import React, { useState, useEffect } from 'react';
import { Redirect, useLocation } from 'react-router-dom';
import { connect } from 'react-redux';
import { googleAuthenticate } from '../actions/auth';
import queryString from 'query-string';

const Google = ({ googleAuthenticate }) => {
    let location = useLocation();
    const [redirectTo, setRedirectTo] = useState('');

    useEffect(() => {
        const { state, code, role } = queryString.parse(location.search);

        if (state && code) {
            googleAuthenticate(state, code);
            setRedirectTo(role === 'secretary' ? '/secretary' : '/student');
        }
    }, [location.search]);

    if (redirectTo) {
        return <Redirect to={redirectTo} />;
    }

    return null; 
};

const mapStateToProps = (state) => ({
    isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps, { googleAuthenticate })(Google);
