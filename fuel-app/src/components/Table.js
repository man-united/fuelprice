import React from 'react';

const Table = (props) => {
  const map_base = 'https://www.google.com/maps/place/';

  return (
    <div className="bg-white">
      <table className="table table-hover opacity-5">
        <thead className="table-dark">
          <tr>
            <th>Name</th>
            <th>Brand</th>
            <th>Address</th>
            <th>Distance(km)</th>
            <th>Price</th>
            <th>Last Updated</th>
          </tr>
        </thead>
        <tbody>
          {props.data.map((item, index) => {
            const url = map_base.concat(item.address);
            return (
              <tr key={index}>
                <td>{item.name}</td>
                <td>{item.brand}</td>
                <td>
                  <a href={url} target="_blank">
                    {item.address}
                  </a>
                </td>
                <td>{item.distance}</td>
                <td className="text-center text-success">{item.price}</td>
                <td>{item.last_updated}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
