// IngredientCard.tsx
import React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";

interface IngredientCardProps {
  ingredient: string;
  bulletPoints: string[];
  isFlagged: boolean;
  dietaryChangeDescription?: string;
  swapRationales?: string[];
}

const IngredientCard: React.FC<IngredientCardProps> = ({
  ingredient,
  bulletPoints,
  isFlagged,
  dietaryChangeDescription,
  swapRationales,
}) => (
  <Card
    variant="outlined"
    sx={{
      mb: 2,
      borderLeft: isFlagged ? "4px solid #ed6c02" : undefined,
      backgroundColor: "#fffde7",
      boxShadow: 2,
    }}
  >
    <CardContent sx={{ p: 2 }}>
      <Typography
        variant="h6"
        component="div"
        color={isFlagged ? "warning.main" : "text.primary"}
        sx={{ fontWeight: isFlagged ? 700 : 500 }}
      >
        {ingredient}
      </Typography>
      <List dense>
        {bulletPoints.map((bp, idx) => {
          const isRationale = bp.startsWith("Flagged:");
          return (
            <ListItem
              key={idx}
              sx={{
                color: isRationale
                  ? "error.main"
                  : isFlagged
                  ? "text.primary"
                  : "inherit",
                fontWeight: isRationale ? 600 : isFlagged ? 500 : 400,
                fontSize: "1rem",
              }}
              title={isRationale && swapRationales ? swapRationales.join("; ") : ""}
              disableGutters
            >
              {bp}
            </ListItem>
          );
        })}
      </List>
      {isFlagged && dietaryChangeDescription && (
        <Typography variant="caption" color="warning.main" sx={{ mt: 1, display: "block" }}>
          {dietaryChangeDescription}
        </Typography>
      )}
    </CardContent>
  </Card>
);

export default IngredientCard;
