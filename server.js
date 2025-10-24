import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import connectDB from "./config/db.js";
import authRoutes from "./routes/authRoutes.js";
import planRoutes from "./routes/planRoutes.js";
import yogaRoutes from "./routes/yogaRoutes.js";
import interactionRoutes from "./routes/interactionRoutes.js";



dotenv.config();
connectDB();

const app = express();
app.use(cors());
app.use(express.json());

// Routes
app.use("/api/auth", authRoutes);
app.use("/api/plan", planRoutes);
app.use("/api/yoga", yogaRoutes);
app.use("/api/interaction", interactionRoutes);

 

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
