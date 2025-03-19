#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Validating Docker configuration...${NC}"

# Check if Dockerfile exists
if [ -f backend/docker/Dockerfile ]; then
    echo -e "${GREEN}✓ Dockerfile exists at backend/docker/Dockerfile${NC}"
else
    echo -e "${RED}✗ Dockerfile not found at backend/docker/Dockerfile${NC}"
fi

# Check if docker-compose.yml exists
if [ -f backend/docker/docker-compose.yml ]; then
    echo -e "${GREEN}✓ docker-compose.yml exists at backend/docker/docker-compose.yml${NC}"
else
    echo -e "${RED}✗ docker-compose.yml not found at backend/docker/docker-compose.yml${NC}"
fi

# Check if .dockerignore exists
if [ -f backend/docker/.dockerignore ]; then
    echo -e "${GREEN}✓ .dockerignore exists at backend/docker/.dockerignore${NC}"
else
    echo -e "${RED}✗ .dockerignore not found at backend/docker/.dockerignore${NC}"
fi

# Check if app directory exists
if [ -d backend/app ]; then
    echo -e "${GREEN}✓ app directory exists at backend/app${NC}"
else
    echo -e "${RED}✗ app directory not found at backend/app${NC}"
fi

# Check if requirements.txt exists
if [ -f backend/requirements.txt ]; then
    echo -e "${GREEN}✓ requirements.txt exists at backend/requirements.txt${NC}"
else
    echo -e "${RED}✗ requirements.txt not found at backend/requirements.txt${NC}"
fi

# Check docker-compose file references
echo -e "\n${YELLOW}Checking docker-compose.yml references...${NC}"
DOCKERFILE_REF=$(grep -E "dockerfile:.*" backend/docker/docker-compose.yml | awk '{print $2}')
echo -e "Dockerfile reference in docker-compose.yml: ${DOCKERFILE_REF}"

# Full path to referenced Dockerfile from docker-compose
DOCKERFILE_PATH="backend/${DOCKERFILE_REF}"
if [ -f "${DOCKERFILE_PATH}" ]; then
    echo -e "${GREEN}✓ Referenced Dockerfile (${DOCKERFILE_PATH}) exists${NC}"
else
    echo -e "${RED}✗ Referenced Dockerfile (${DOCKERFILE_PATH}) does not exist${NC}"
    echo -e "${YELLOW}Suggestion: Update dockerfile reference in docker-compose.yml to 'dockerfile: Dockerfile'${NC}"
fi

# Check GitHub Actions workflow references
echo -e "\n${YELLOW}Checking GitHub Actions workflow references...${NC}"
if [ -f .github/workflows/docker-image.yml ]; then
    DOCKERFILE_REF_CI=$(grep -E "file:.*Dockerfile" .github/workflows/docker-image.yml | awk '{print $2}')
    echo -e "Dockerfile reference in docker-image.yml: ${DOCKERFILE_REF_CI}"
    if [ -f "${DOCKERFILE_REF_CI}" ]; then
        echo -e "${GREEN}✓ Referenced Dockerfile (${DOCKERFILE_REF_CI}) in GitHub Actions exists${NC}"
    else
        echo -e "${RED}✗ Referenced Dockerfile (${DOCKERFILE_REF_CI}) in GitHub Actions does not exist${NC}"
    fi
else
    echo -e "${YELLOW}docker-image.yml workflow not found${NC}"
fi

echo -e "\n${YELLOW}Validation complete!${NC}" 