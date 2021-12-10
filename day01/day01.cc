#include <fstream>
#include <iostream>
#include <iterator>
#include <string>
#include <vector>

static const std::string DEFAULT_INPUT_FILE_NAME = "input";

std::vector<int> readInputData(const std::string& inputFileName) {
    auto inputFile = std::ifstream{inputFileName};
    auto inputStart = std::istream_iterator<int>{inputFile};
    auto inputEnd = std::istream_iterator<int>{};
    return std::vector<int>{inputStart, inputEnd};
}

std::vector<int> concatenateMeasurementsInTriplets(const std::vector<int>& measurements) {
    auto concatenatedMeasurements = std::vector<int>{};
    for (size_t i = 0; i < measurements.size() - 2; ++i) {
        const auto concatenatedMeasurement = measurements[i] + measurements[i + 1] + measurements[i + 2];
        concatenatedMeasurements.push_back(concatenatedMeasurement);
    }
    return concatenatedMeasurements;
}

int getNumberOfIncrements(const std::vector<int>& measurements) {
    auto previousMeasurement = measurements.front();
    auto numberOfIncreases = 0;
    for (const auto measurement : measurements) {
        if (measurement > previousMeasurement) {
            ++numberOfIncreases;
        }
        previousMeasurement = measurement;
    }
    return numberOfIncreases;
}

void part1(const std::vector<int>& measurements) {
    std::cout << "Running part 1..." << std::endl;
    const auto numberOfIncrements = getNumberOfIncrements(measurements);
    std::cout << "Result is: " << numberOfIncrements << std::endl;
    std::cout << std::endl;
}

void part2(const std::vector<int>& measurements) {
    std::cout << "Running part 2..." << std::endl;
    const auto concatenatedMeasurements = concatenateMeasurementsInTriplets(measurements);
    const auto numberOfIncrements = getNumberOfIncrements(concatenatedMeasurements);
    std::cout << "Result is: " << numberOfIncrements << std::endl;
    std::cout << std::endl;
}

int main(int argc, char *argv[]) {
    const auto inputFileName = argc == 2 ? argv[1] : DEFAULT_INPUT_FILE_NAME;
    const auto measurements = readInputData(inputFileName);
    part1(measurements);
    part2(measurements);
}
