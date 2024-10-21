import mongoose from 'mongoose';

const parkingSpotSchema = new mongoose.Schema({
  areaName: {
    type: String,
    required: true,
  },
  spotNumber: {
    type: String,
    required: true,
    unique: true,
  },
  isOccupied: {
    type: Boolean,
    default: false,
  },
  carType: {
    type: String,
    enum: ['small', 'medium', 'large'],  // Adjust based on your needs
    required: true,
  },
});

const ParkingSpot = mongoose.model('ParkingSpot', parkingSpotSchema);

export default ParkingSpot;
