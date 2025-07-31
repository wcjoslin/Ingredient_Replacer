// DietSummaryCard.tsx
import React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";

interface DietSummaryCardProps {
  name: string;
  description: string;
  categoryRestrictions: { text: string; full: string }[];
  macronutrientRestrictions: { text: string; full: string }[];
}

const DietSummaryCard: React.FC<DietSummaryCardProps> = ({
  name,
  description,
  categoryRestrictions,
  macronutrientRestrictions,
}) => (
  <Card variant="outlined" sx={{ mb: 2, boxShadow: 2 }}>
    <CardContent sx={{ p: 2 }}>
      <Typography variant="h6" component="div" sx={{ fontWeight: 700 }}>
        {name}
      </Typography>
      <Typography variant="body2" sx={{ mb: 1 }}>
        {description}
      </Typography>
      <div>
        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
          Category Restrictions:
        </Typography>
        <List dense>
          {categoryRestrictions.map((r, i) => (
            <ListItem
              key={i}
              title={r.full}
              sx={{ pl: 2, fontSize: "1rem" }}
              disableGutters
            >
              {r.text}
              {r.text !== r.full && (
                <Typography
                  component="span"
                  variant="caption"
                  sx={{ ml: 1, color: "text.secondary" }}
                >
                  (…)
                </Typography>
              )}
            </ListItem>
          ))}
        </List>
      </div>
      <div>
        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
          Macronutrient Restrictions:
        </Typography>
        <List dense>
          {macronutrientRestrictions.map((r, i) => (
            <ListItem
              key={i}
              title={r.full}
              sx={{ pl: 2, fontSize: "1rem" }}
              disableGutters
            >
              {r.text}
              {r.text !== r.full && (
                <Typography
                  component="span"
                  variant="caption"
                  sx={{ ml: 1, color: "text.secondary" }}
                >
                  (…)
                </Typography>
              )}
            </ListItem>
          ))}
        </List>
      </div>
    </CardContent>
  </Card>
);

export default DietSummaryCard;
