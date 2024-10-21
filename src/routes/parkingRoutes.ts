import express from 'express';
import ParkingSpot from '../models/ParkingSpot';

const router = express.Router();

// Create a new parking spot
router.post('/parking', async (req, res) => {
  const { areaName, spotNumber, carType } = req.body;
  try {
    const parkingSpot = new ParkingSpot({ areaName, spotNumber, carType });
    await parkingSpot.save();
    res.status(201).json(parkingSpot);
  } catch (error) {
    if (error instanceof Error) {
        res.status(400).json({ error: error.message });
      } else {
        res.status(400).json({ error: 'An unknown error occurred' });
      }
  }
});

// Get all parking spots
router.get('/parking', async (req, res) => {
  try {
    const parkingSpots = await ParkingSpot.find();
    res.status(200).json(parkingSpots);
  } catch (error) {
    if (error instanceof Error) {
        res.status(400).json({ error: error.message });
      } else {
        res.status(400).json({ error: 'An unknown error occurred' });
      }
  }
});

export default router;
