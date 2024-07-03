// InfoBox.tsx
import React from 'react';
import { Popover, Typography, Box } from '@mui/material';

type InfoObject = {
    [key: string]: string | InfoObject;
};

interface InfoBoxProps {
    info: InfoObject;
    anchorEl: HTMLElement | null;
    onClose: () => void;
}

const InfoBox: React.FC<InfoBoxProps> = ({ info, anchorEl, onClose }) => {
    const open = Boolean(anchorEl);
    const id = open ? 'info-popover' : undefined;

    const renderInfo = (info: InfoObject, level: number = 0) => {
        if (!info || typeof info !== 'object') {
            return null; // o un mensaje de error adecuado
          }
        return (
            <Box ml={level * 2}>
                {Object.entries(info).map(([key, value]) => (
                    <Box key={key} my={1}>
                        <Typography variant="body1" component="span" fontWeight="bold">
                            {key}:
                        </Typography>
                        {typeof value === 'string' ? (
                            <Typography variant="body1" component="span" ml={1}>
                                {value}
                            </Typography>
                        ) : (
                            <Box ml={2}>
                                {renderInfo(value as InfoObject, level + 1)}
                            </Box>
                        )}
                    </Box>
                ))}
            </Box>
        );
    };

    return (
        <Popover
            id={id}
            open={open}
            anchorEl={anchorEl}
            onClose={onClose}
            anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
            }}
            transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
            }}
        >
            <Box p={2} maxWidth={300}>
                {renderInfo(info)}
            </Box>
        </Popover>
    );
};

export default InfoBox;
