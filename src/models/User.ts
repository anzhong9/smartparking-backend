import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
    unique: true,
  },
  loyaltyPoints: {
    type: Number,
    default: 0,
  },
  parkingHistory: [{
    parkingSpotId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'ParkingSpot',
    },
    date: {
      type: Date,
      default: Date.now,
    },
  }],
});

const User = mongoose.model('User', userSchema);

export default User;
