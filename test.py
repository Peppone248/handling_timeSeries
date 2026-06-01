public static void DoInterpolation_SampleAndHold(ref double[] inputVec, ref double[] inputTS, int outputFreq, double timeBegin, double timeEnd, ref double[] outputVec
)
        {
            int outputLength = outputVec.Length;
            double timeStep = 1.0 / outputFreq;
            double currentTime = timeBegin;

            uint idx = 1;
            const double noRx = double.NaN;

            double firstTS = inputTS[0];
            double lastTS = inputTS[inputTS.Length - 1];
            double lastVal = inputVec[inputVec.Length - 1];

            for (int i = 0; i < outputLength; i++)
            {
                if (currentTime < firstTS)
                {
                    // Before the first known timestamp — fill with NaN
                    outputVec[i] = noRx;
                }
                else if (currentTime >= lastTS)
                {
                    // After the last known timestamp — hold last value
                    outputVec[i] = lastVal;
                }
                else
                {
                    // Advance index if needed
                    while (idx < inputTS.Length && inputTS[idx] <= currentTime)
                    {
                        idx++;
                    }

                    if (idx == 0)
                    {
                        outputVec[i] = inputVec[0];
                    }
                    else
                    {
                        outputVec[i] = inputVec[idx - 1]; // sample-and-hold
                    }
                }

                currentTime += timeStep;
            }
        }