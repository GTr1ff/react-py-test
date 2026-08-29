import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import App from "./App";

describe("App", () => {
  it("renders the project landing page", () => {
    render(<App />);
    expect(screen.getByText(/start building\./i)).toBeInTheDocument();
  });
});
