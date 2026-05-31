import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import LandingPage from "./page";

describe("LandingPage", () => {
  it("renders the hero heading", () => {
    render(<LandingPage />);
    expect(
      screen.getByRole("heading", { name: /your routine bugs fix themselves/i })
    ).toBeInTheDocument();
  });

  it("renders all three feature cards", () => {
    render(<LandingPage />);
    expect(screen.getAllByText("Instant Analysis").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Autonomous Code Generation").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Human-in-the-Loop Review").length).toBeGreaterThanOrEqual(1);
  });

  it("renders the four how-it-works steps", () => {
    render(<LandingPage />);
    expect(screen.getAllByText("Label an issue").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("AI analyzes").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Code generated").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("PR created").length).toBeGreaterThanOrEqual(1);
  });

  it("renders the GitHub sign-in link", () => {
    render(<LandingPage />);
    expect(screen.getAllByText("Sign in with GitHub").length).toBeGreaterThanOrEqual(1);
  });
});
