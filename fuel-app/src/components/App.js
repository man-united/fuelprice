import React, { useState } from 'react';
import axios from 'axios';
import Form from './Form';
import Table from './Table';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

const App = () => {
  const [data, setData] = useState([]);
  const [inputField, setInputField] = useState({
    location: '',
    fuel: 'U91',
    distance: 1,
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    axios({
      method: 'post',
      url: '/api',
      timeout: 4000,
      data: {
        location: inputField.location,
        fuel: inputField.fuel,
        distance: inputField.distance,
      },
    })
      .then((response) => {
        setData(response.data.result);
        console.log(response);
      })
      .catch((error) => console.log(error));
  };

  return (
    <div className="main p-5 min-vh-100 ">
      <Form inputField={inputField} setInputField={setInputField} handleSubmit={handleSubmit} />
      {<Table data={data} />}
    </div>
  );
};

export default App;
