export const getBusListData = async () => {
	const apiUrl = 'http://localhost:8000/bus/list';
	var response;
	await fetch(apiUrl)
		.then((res) => {
			if (!res.ok) {
				throw new Error('Network resonse was not ok');
			}
			const response = res.json();
			return response;
		})
		.then((body) => {
			response = body;
		})
		.catch((err) => {
			console.log('===> error getBusList ', err);
			var bus_list = document.getElementById('bus_list');
			bus_list.innerText = 'There are no buses.';
		});
	return response;
};

export const getBusList = async () => {
	const buses = await getBusListData();
	var bus_list = document.getElementById('bus_list');
	if (buses.length == 0) {
		bus_list.innerText = 'There are no buses.';
	} else {
		// create bus list
		buses.forEach((x) => {
			var bus = document.createElement('div');
			bus.id = x.id;
			bus.className = 'row p-2';
			var number = document.createElement('div');
			number.className = 'col-1';
			number.innerText = x.number;
			var driver_name = document.createElement('div');
			driver_name.className = 'col-3';
			driver_name.innerText = x.driver_name;
			var seats = document.createElement('div');
			seats.id = 'seats_' + x.id;
			seats.className = 'col-3';
			seats.innerText = x.available_seats + ' / ' + x.max_seats;
			var status = document.createElement('div');
			status.className = 'col-2';
			status.innerText = x.status_display;
			var action = document.createElement('div');
			action.className = 'col-3';
			var button = document.createElement('button');
			button.id = 'action_' + x.id;
			button.onclick = () => reserveSeat(x.id, 1);
			// button.addEventListener('click', () => reserveSeat(x.id, 1));
			button.innerText = 'Reserve';
			if (x.available_seats == 0) {
				button.disabled = true;
				button.innerText = 'No seats available';
				bus.className += ' bg-danger';
			} else if (x.available_seats < 10) {
				bus.className += ' bg-warning';
			} else if (x.status == 2 || x.status == 3) {
				bus.className += ' bg-info';
			} else if (x.status == 0 || x.status == 1) {
				bus.className += ' bg-success';
			} else {
			}
			action.appendChild(button);

			bus.appendChild(number);
			bus.appendChild(driver_name);
			bus.appendChild(seats);
			bus.appendChild(status);
			bus.appendChild(action);

			bus_list.appendChild(bus);
		});
	}
};

// reserve or unreserve seat: flag=1 -> reserve, flag=-1 -> unreserve
export const reserveSeat = async (busId, flag) => {
	const apiUrl = 'http://localhost:8000/bus/reserve';
	await fetch(apiUrl, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ id: busId, flag: flag }),
	})
		.then((res) => {
			const response = res.json();
			if (!res.ok) {
				console.log(response.body);
			}
			return response;
		})
		.then((body) => {
			console.log(body);
			if (body.status == 'success') {
				alert('Seat ' + flag == 1 ? 'reserved' : 'unreserved' + ' successfully!');
				// reset the available seats
				var bus_seats = document.getElementById('seats_' + busId);
				bus_seats.innerText = body.data.available_seats + ' / ' + body.data.max_seats;
				// reset the action (1: reserve action, -1: unreserve action)
				var bus_action = document.getElementById('action_' + busId);
				bus_action.onclick = () => reserveSeat(busId, flag * -1);
				bus_action.innerText = flag == 1 ? 'Unreserve' : 'Reserve';
			}
		})
		.catch((err) => {
			console.log('===> error reserveSeat ', err);
			response = false;
		});
};

if (typeof window !== 'undefined') {
	window.onload = () => {
		console.log('Welcome Bus Station');
		getBusList();
	};
}
