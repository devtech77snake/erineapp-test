import { JSDOM } from 'jsdom';
import { expect } from 'chai';
import { getBusListData, reserveSeat } from '../app.js';
import sinon from 'sinon';
import fetch from 'node-fetch';

const { window } = new JSDOM('<!doctype html><html><body></body></html>');
global.window = window;
global.document = window.document;

global.fetch = fetch;
global.alert = (message) => message;

describe('Bus Station App', () => {
	describe('getBusListData', () => {
		it('fetch bus list data', async () => {
			const mockData = [{ id: 1, number: 'Bus 1', driver_name: 'John Doe', available_seats: 20, max_seats: 30, status_display: 'In Service' }];

			sinon.stub(global, 'fetch').resolves({
				ok: true,
				json: async () => mockData,
			});

			const buses = await getBusListData();
			expect(buses).to.eql(mockData);

			global.fetch.restore();
		});
	});
});

describe('Bus Station App', () => {
	var fetchStub;

	beforeEach(() => {
		// Set up DOM elements needed for the reserveSeat function
		const busList = document.createElement('div');
		busList.id = 'bus_list';
		document.body.appendChild(busList);

		const bus = document.createElement('div');
		bus.id = '1';
		bus.className = 'row p-2';

		const seats = document.createElement('div');
		seats.id = 'seats_1';
		seats.className = 'col-3';
		seats.innerText = '20 / 30';
		bus.appendChild(seats);

		const action = document.createElement('div');
		action.className = 'col-3';
		const button = document.createElement('button');
		button.id = 'action_1';
		action.appendChild(button);
		bus.appendChild(action);

		busList.appendChild(bus);

		// Set up the fetch stub
		fetchStub = sinon.stub(global, 'fetch');
	});

	afterEach(() => {
		fetchStub.restore();
		document.body.innerHTML = '';
	});

	describe('reserveSeat', () => {
		// when reserve seat
		it('should reserve a seat successfully', async () => {
			const busId = 1;
			const flag = 1;
			const expectedSeatsText = '19 / 30';

			fetchStub.resolves({
				ok: true,
				json: async () => ({
					status: 'success',
					data: {
						available_seats: 19,
						max_seats: 30,
					},
				}),
			});

			await reserveSeat(busId, flag);

			const seatsElement = document.getElementById('seats_1');
			expect(seatsElement.innerText).to.equal(expectedSeatsText);

			const actionButton = document.getElementById('action_' + busId);
			expect(actionButton.innerText).to.equal('Unreserve');
		});

		// when unreserve seat
		it('should unreserve a seat successfully', async () => {
			const busId = 1;
			const flag = -1;
			const expectedSeatsText = '21 / 30';

			fetchStub.resolves({
				ok: true,
				json: async () => ({
					status: 'success',
					data: {
						available_seats: 21,
						max_seats: 30,
					},
				}),
			});

			await reserveSeat(busId, flag);

			const seatsElement = document.getElementById('seats_1');
			expect(seatsElement.innerText).to.equal(expectedSeatsText);

			const actionButton = document.getElementById('action_' + busId);
			expect(actionButton.innerText).to.equal('Reserve');
		});
	});
});
