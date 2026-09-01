\# MuveFit — System Architecture



\## Overview



MuveFit is a camera-based movement analysis platform combining a React frontend, backend services, exercise-analysis scripts, and pose-estimation models.



\## High-Level Architecture



```text

User

&#x20; ↓

Camera / Webcam

&#x20; ↓

React Frontend

&#x20; ↓

Backend API

&#x20; ↓

Exercise / AI Service

&#x20; ↓

Python + MediaPipe

&#x20; ↓

Pose Landmarks

&#x20; ↓

Movement Analysis

&#x20; ↓

Structured Exercise Result

&#x20; ↓

Backend

&#x20; ↓

React Dashboard / Report

