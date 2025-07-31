// SwapSuggestionCard.tsx
import React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";

interface RankedSwap {
  substitute: string;
  score: number;
}

interface SwapSuggestionCardProps {
  original: string;
  rankedSwaps: RankedSwap[];
}

const SwapSuggestionCard: React.FC<SwapSuggestionCardProps> = ({
  original,
  rankedSwaps,
}) => (
  <Card variant="outlined" sx={{ mb: 2, boxShadow: 2 }}>
    <CardContent sx={{ p: 2 }}>
      <Typography variant="h6" component="div" sx={{ fontWeight: 700 }}>
        {original}
      </Typography>
      {rankedSwaps.length > 0 ? (
        <List dense>
          {rankedSwaps.map((s, idx) => (
            <ListItem
              key={idx}
              sx={{ pl: 2, fontSize: "1rem" }}
              disableGutters
            >
              {s.substitute}{" "}
              <Typography
                component="span"
                variant="caption"
                sx={{ ml: 1, color: "text.secondary" }}
              >
                (score: {s.score.toFixed(2)})
              </Typography>
            </ListItem>
          ))}
        </List>
      ) : (
        <Typography color="error.main" sx={{ mt: 1 }}>
          No swap found
        </Typography>
      )}
    </CardContent>
  </Card>
);

export default SwapSuggestionCard;
