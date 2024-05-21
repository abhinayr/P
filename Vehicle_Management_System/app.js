function refreshVehicleList() {
  fetch('http://localhost:8000/vehicles/')
    .then(response => response.json())
    .then(data => {
      const vehicleList = document.getElementById('vehicle-list');
      vehicleList.innerHTML = '';
      Object.values(data).forEach(vehicle => {
        const vehicleDiv = document.createElement('div');
        vehicleDiv.innerHTML = `
          <h2>Vehicle List</h2>
          <p>ID: ${vehicle.id}</p>
          <p>Model: ${vehicle.make} ${vehicle.model}</p>
          <p>Year: ${vehicle.year}</p>
          <p>Price: ${vehicle.price}</p>
          <p>Sold: ${vehicle.is_sold ? 'Yes' : 'No'}</p>
        `;
        vehicleList.appendChild(vehicleDiv);
      });
    });
}

function searchVehicle() {
  const id = document.getElementById('search-id').value;
  fetch(`http://localhost:8000/vehicles/${id}`)
    .then(response => response.json())
    .then(data => {
      const vehicleList = document.getElementById('vehicle-list');
      vehicleList.innerHTML = '';
      const vehicleDiv = document.createElement('div');
      vehicleDiv.innerHTML = `
        <h2>${data.make} ${data.model}</h2>
        <p>Year: ${data.year}</p>
        <p>Price: ${data.price}</p>
        <p>Sold: ${data.is_sold ? 'Yes' : 'No'}</p>
      `;
      vehicleList.appendChild(vehicleDiv);
    });
}

function deleteVehicle() {
  const id = document.getElementById('delete-id').value;
  fetch(`http://localhost:8000/vehicles/${id}`, {
    method: 'DELETE',
  })
  .then(response => response.json())
  .then(data => {
    refreshVehicleList();
  });
}

window.onload = function() {
  refreshVehicleList();

  const addVehicleForm = document.getElementById('add-vehicle-form');
  addVehicleForm.onsubmit = function(e) {
  e.preventDefault();

  const make = document.getElementById('make').value;
  const model = document.getElementById('model').value;
  const year = document.getElementById('year').value;
  const price = document.getElementById('price').value;

  fetch('http://localhost:8000/vehicles/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      make: make,
      model: model,
      year: parseInt(year),
      price: parseFloat(price),
    }),
  })
  .then(response => response.json())
  .then(data => {
    refreshVehicleList();
    alert('Vehicle added successfully!');
  });
};

  const editVehicleForm = document.getElementById('edit-vehicle-form');
  editVehicleForm.onsubmit = function(e) {
    e.preventDefault();

    const id = document.getElementById('edit-id').value;
    const make = document.getElementById('edit-make').value;
    const model = document.getElementById('edit-model').value;
    const year = document.getElementById('edit-year').value;
    const price = document.getElementById('edit-price').value;

    fetch(`http://localhost:8000/vehicles/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        make: make,
        model: model,
        year: parseInt(year),
        price: parseFloat(price),
      }),
    })
    .then(response => response.json())
    .then(data => {
      refreshVehicleList();
    });
  };
};

const classifyForm = document.getElementById('classify-form');
classifyForm.onsubmit = function(e) {
    e.preventDefault();

    const image = document.getElementById('image').files[0];
    const formData = new FormData();
    formData.append('file', image);

    fetch('http://localhost:8000/classify/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('classification-result');
        if (data.is_car) {
            resultDiv.innerHTML = '<p>This is an image of a car</p>';
        } else {
            resultDiv.innerHTML = '<p>There is no car in the image</p>';
        }
    })
    .catch(error => {
        const resultDiv = document.getElementById('classification-result');
        resultDiv.innerHTML = `<p>Error occurred while classifying the image: ${error.message}</p>`;
    });
};
