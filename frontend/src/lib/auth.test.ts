import { beforeEach, describe, expect, it } from "vitest";

import { getToken, isAuthenticated } from "./auth";

describe("auth", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  describe("getToken", () => {
    it("returns null when no token is stored", () => {
      expect(getToken()).toBeNull();
    });

    it("returns the stored token", () => {
      localStorage.setItem("ticketforge_token", "test-jwt");
      expect(getToken()).toBe("test-jwt");
    });
  });

  describe("isAuthenticated", () => {
    it("returns false when no token exists", () => {
      expect(isAuthenticated()).toBe(false);
    });

    it("returns true when a token exists", () => {
      localStorage.setItem("ticketforge_token", "test-jwt");
      expect(isAuthenticated()).toBe(true);
    });
  });
});
