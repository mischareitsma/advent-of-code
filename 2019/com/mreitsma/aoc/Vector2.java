package com.mreitsma.aoc;

import java.util.Objects;

public class Vector2 {

    public static final Vector2 ZERO = new Vector2(0, 0);
    public final double x;
    public final double y;

    public Vector2(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public double manhattanDistance(Vector2 v) {
        return Math.abs(x - v.x) + Math.abs(y - v.y);
    }

    public Vector2 add(Vector2 v) {
        return new Vector2(x + v.x, y + v.y);
    }

    public Vector2 add(double dx, double dy) {
        return new Vector2(x + dx, y + dy);
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        Vector2 vector2 = (Vector2) o;
        return Double.compare(x, vector2.x) == 0 && Double.compare(y, vector2.y) == 0;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }

    @Override
    public String toString() {
        return "Vector2{" + "x=" + x + ", y=" + y + "}";
    }
}
