// Copyright 2009-2019 NTESS. Under the terms
// of Contract DE-NA0003525 with NTESS, the U.S.
// Government retains certain rights in this software.
//
// Copyright (c) 2009-2019, NTESS
// All rights reserved.
//
// Portions are copyright of other developers:
// See the file CONTRIBUTORS.TXT in the top level directory
// the distribution for more information.
//
// This file is part of the SST software package. For license
// information, see the LICENSE file in the top level directory of the
// distribution.


#ifndef _H_SST_ELEMENTS_EMBER_AMR_TEXT_FILE
#define _H_SST_ELEMENTS_EMBER_AMR_TEXT_FILE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ember3damrfile.h"

namespace SST {
    namespace Ember {

        class EmberAMRTextFile : public EmberAMRFile {

        public:
            EmberAMRTextFile(char *amrPath, Output *out) :
                EmberAMRFile(amrPath, out) {

                amrFile = fopen(amrFilePath, "rt");

                if (nullptr == amrFile) {
                    output->fatal(CALL_INFO, -1, "Unable to open file: %s\n", amrPath);
                }

                char *headerLine = readLine();

                if (nullptr == headerLine) {
                    output->fatal(CALL_INFO, -1,
                                  "Error reading header file for AMR blocks in: %s\n", amrPath);
                }

                char *blockCountStr = strtok(headerLine, " ");
                char *refineLevelStr = strtok(nullptr, " ");
                char *blocksXStr = strtok(nullptr, " ");
                char *blocksYStr = strtok(nullptr, " ");
                char *blocksZStr = strtok(nullptr, " ");

                totalBlockCount = atoi(blockCountStr);
                maxRefinementLevel = atoi(refineLevelStr);
                blocksX = atoi(blocksXStr);
                blocksY = atoi(blocksYStr);
                blocksZ = atoi(blocksZStr);

                out->verbose(CALL_INFO, 8, 0, "Read mesh header info: blocks=%"
                PRIu32
                ", max-lev: %"
                PRIu32
                " bkX=%"
                PRIu32
                ", blkY=%"
                PRIu32
                ", blkZ=%"
                PRIu32
                "\n",
                    totalBlockCount, maxRefinementLevel, blocksX, blocksY, blocksZ);
            }

            ~EmberAMRTextFile() {

            }

            bool isBinary() {
                return false;
            }

            char *readLine() {
                char *theLine = (char *) malloc(sizeof(char) * 64);
                int nextIndex = 0;
                char nextChar;

                while ((nextChar = fgetc(amrFile)) != '\n' && (nextChar != EOF)) {
                    theLine[nextIndex] = nextChar;
                    nextIndex++;
                }

                theLine[nextIndex] = '\0';

                output->verbose(CALL_INFO, 32, 0, "Read line: %s\n", theLine);

                return theLine;
            }

            void readNodeMeshLine(uint32_t *blockCount) {
                char *nextLine = readLine();

                *blockCount = (uint32_t) atoi(nextLine);

                free(nextLine);
            }

            void readNextMeshLine(uint32_t *blockID, uint32_t *refineLev,
                                  int32_t *xDown, int32_t *xUp,
                                  int32_t *yDown, int32_t *yUp,
                                  int32_t *zDown, int32_t *zUp) {

                char *nextLine = readLine();

                char *blockIDStr = strtok(nextLine, " ");
                char *refineLevelStr = strtok(nullptr, " ");
                char *xDStr = strtok(nullptr, " ");
                char *xUStr = strtok(nullptr, " ");
                char *yDStr = strtok(nullptr, " ");
                char *yUStr = strtok(nullptr, " ");
                char *zDStr = strtok(nullptr, " ");
                char *zUStr = strtok(nullptr, " ");

                *blockID = (uint32_t) atoi(blockIDStr);
                *refineLev = (uint32_t) atoi(refineLevelStr);
                *xDown = (int32_t) atoi(xDStr);
                *xUp = (int32_t) atoi(xUStr);
                *yDown = (int32_t) atoi(yDStr);
                *yUp = (int32_t) atoi(yUStr);
                *zDown = (int32_t) atoi(zDStr);
                *zUp = (int32_t) atoi(zUStr);

                free(nextLine);
            }

        private:
            FILE *amrFile;
        };

    }
}

#endif
