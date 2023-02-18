import React from 'react';
import { Button } from 'react-bootstrap';

const Form = (props) => {
  const handleInput = (e) => {
    const { name, value } = e.target;
    props.setInputField((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <form onSubmit={props.handleSubmit} className="p-2 mb-4 border rounded bg-white">
      <div className="row mb-3">
        <label className="col-sm-2 col-form-label">Location:</label>
        <div className="col-sm-4">
          <input
            className="form-control"
            type="text"
            name="location"
            placeholder="Suburb or Postcode"
            onChange={handleInput}
            value={props.inputField.location}
          ></input>
        </div>
      </div>

      <div className="row mb-3">
        <label className="col-sm-2 col-form-label">Fuel Type:</label>
        <div className="col-sm-4">
          <select className="form-select" name="fuel" value={props.inputField.fuel} onChange={handleInput}>
            <option value="U91">(U91) Unleaded</option>
            <option value="P95">(P95) Premium Unleaded</option>
            <option value="P98">(P98) Premium Unleaded</option>
            <option value="DL">(DL) Diesel</option>
            <option value="PDL">(PDL) Premium Diesel</option>
            <option value="E10">(E10) Ethanol</option>
            <option value="E85">(E85) Ethanol</option>
            <option value="LPG">(LPG) Liquified Petroleum Gas</option>
            <option value="EV">(EV) Electric Vehicle</option>
          </select>
        </div>
      </div>

      <div className="row mb-3">
        <label className="col-sm-2 col-form-label">Max Distance(km):</label>
        <div className="col-sm-2">
          <input
            className="form-control"
            type="number"
            name="distance"
            placeholder="distance in km"
            onChange={handleInput}
            value={props.inputField.distance}
          ></input>
        </div>
      </div>

      <div className="col-md-2">
        <Button className="btn btn-primary" type="submit">
          Submit
        </Button>
      </div>
    </form>
  );
};

export default Form;
