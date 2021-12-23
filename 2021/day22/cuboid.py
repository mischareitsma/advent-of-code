from dataclasses import dataclass

def find_mergable_cuboids(cuboids: list['Cuboid']) -> tuple:
    for c1 in cuboids:
        for c2 in cuboids:
            # Mergable if two of the sides are identical and the third
            # touches

            x = (c1.xi == c2.xi) and (c1.xf == c2.xf)
            y = (c1.yi == c2.yi) and (c1.yf == c2.yf)
            z = (c1.zi == c2.zi) and (c1.zf == c2.zf)

            x_touch = (c1.xi - 1 == c2.xf) or (c2.xi - 1 == c1.xf)
            y_touch = (c1.yi - 1 == c2.yf) or (c2.yi - 1 == c1.yf)
            z_touch = (c1.zi - 1 == c2.zf) or (c2.zi - 1 == c1.zf)

            if x and y and z_touch:
                return c1, c2, 'z'
            if x and z and y_touch:
                return c1, c2, 'y'
            if y and z and x_touch:
                return c1, c2, 'x'

    return None, None, None

def get_non_overlapping_range(i, f, oi, of) -> list[tuple[int]]:
    """Get a non overlapping range between the init and final (i, f),
    and the other or overlapping init and final (oi, of).
    """
    ranges = []

    if (oi > i):
        ranges.append((i, oi - 1))
    if (of < f):
        ranges.append((of + 1, f))

    return ranges


def reduce_cuboid_list(cuboids: list['Cuboid']):
    """Reduce the amount of cuboids in the list by merging those that
    can be merged."""

    while True:
        c1, c2, side = find_mergable_cuboids(cuboids)
        if not c1:
            break

        xi = c1.xi
        xf = c1.xf
        yi = c1.yi
        yf = c1.yf
        zi = c1.zi
        zf = c1.zf

        if side == 'x':
            xi = min(c1.xi, c2.xi)
            xf = max(c1.xf, c2.xf)
        if side == 'y':
            yi = min(c1.yi, c2.yi)
            yf = max(c1.yf, c2.yf)
        if side == 'z':
            zi = min(c1.zi, c2.zi)
            zf = max(c1.zf, c2.zf)

        cuboids.remove(c1)
        cuboids.remove(c2)
        cuboids.append(Cuboid(xi, xf, yi, yf, zi, zf))


@dataclass(frozen=True)
class Cuboid:
    xi: int
    xf: int
    yi: int
    yf: int
    zi: int
    zf: int

    def contains(self, other: 'Cuboid') -> bool:
        return (
            self.xi <= other.xi and self.xf >= other.xf and
            self.yi <= other.yi and self.yf >= other.yf and
            self.zi <= other.zi and self.zf >= other.zf
        )

    def split_if_overlap(self, other: 'Cuboid') -> tuple[list['Cuboid'], bool]:
        """Split the cuboid if there is overlap with an incoming cuboid.
        This method returns a list of resulting cuboids without overlap,
        and a boolean indicating that there is overlap. This method
        can retrun `[], True` in case the original cuboid is fully
        absorbed in the other.
        """

        # TODO could also return [] if contains and [self] if no overlap

        if other.contains(self):
            return [], True

        oc = self.get_overlap_cuboid(other)

        if not oc:
            return [], False

        split_cuboids: list['Cuboid'] = []

        # Returns depend on the type of overlap: corner chipped off, a resulting
        # 'stair' or a 'plane'
        # Even more complex, can also chip from the middle, or cut in half

        # Following can be less loops probably, but this is how I drew it on
        # paper :-)

        non_overlap_x = get_non_overlapping_range(self.xi, self.xf, oc.xi, oc.xf)
        non_overlap_y = get_non_overlapping_range(self.yi, self.yf, oc.yi, oc.yf)
        non_overlap_z = get_non_overlapping_range(self.zi, self.zf, oc.zi, oc.zf)

        # All non-overlapping corners, total of 2*2*2 = 8
        for xr in non_overlap_x:
            for yr in non_overlap_y:
                for zr in non_overlap_z:
                    split_cuboids.append(Cuboid(xr[0], xr[1], yr[0], yr[1], zr[0], zr[1]))

        # All non-overlap in two sides, and overalp in one, total of 3 * (2 * 2) = 3 * 4 = 12
        for xr in non_overlap_x:
            for yr in non_overlap_y:
                split_cuboids.append(Cuboid(xr[0], xr[1], yr[0], yr[1], oc.zi, oc.zf))

        for xr in non_overlap_x:
            for zr in non_overlap_z:
                split_cuboids.append(Cuboid(xr[0], xr[1], oc.yi, oc.yf, zr[0], zr[1]))


        for yr in non_overlap_y:
            for zr in non_overlap_z:
                split_cuboids.append(Cuboid(oc.xi, oc.xf, yr[0], yr[1], zr[0], zr[1]))

        # All non-overlap in one side, and overalp in one, total of 3 * 2 = 6
        for xr in non_overlap_x:
            split_cuboids.append(Cuboid(xr[0], xr[1], oc.yi, oc.yf, oc.zi, oc.zf))

        for yr in non_overlap_y:
            split_cuboids.append(Cuboid(oc.xi, oc.xf, yr[0], yr[1], oc.zi, oc.zf))

        for zr in non_overlap_z:
            split_cuboids.append(Cuboid(oc.xi, oc.xf, oc.yi, oc.yf, zr[0], zr[1]))

        # Now we have a max of 8 + 12 + 6 = 26 new cubes, which is in line with the 3*3*3 = 27 - 1
        
        reduce_cuboid_list(split_cuboids)
        return split_cuboids, True

    def get_overlap_range(self, i, f, oi, of) -> tuple:
        """Get overlap in two ranges.
        """
        # Two cases with no overlap:
        if (i > of) or (f < oi):
            return 0, 0, False

        return max([i, oi]), min([f, of]), True

    def get_trimmed_range(self, i, f, oi, of) -> tuple[int]:
        """Get a trimmed range.
        
        This method returns a range that is trimmed. It assumes there
        is already overlap between i,f and oi,of
        """
        return (of + 1, f) if i == oi else (i, oi - 1)

    def get_overlap_cuboid(self, other: 'Cuboid') -> 'Cuboid':
            oxi, oxf, has_x_overlap = self.get_overlap_range(self.xi, self.xf, other.xi, other.xf)
            oyi, oyf, has_y_overlap = self.get_overlap_range(self.yi, self.yf, other.yi, other.yf)
            ozi, ozf, has_z_overlap = self.get_overlap_range(self.zi, self.zf, other.zi, other.zf)

            if has_x_overlap and has_y_overlap and has_z_overlap:
                return Cuboid(oxi, oxf, oyi, oyf, ozi, ozf)
            else:
                return None

    def count_overlap(self, others: list['Cuboid']) -> int:
        """Count the number of overlapping spaces in the cuboid
        compared to other cuboids in the list.
        
        This requires the list to not contain overlapping cuboids!
        """

        overlap = 0

        for c in others:
            oc = self.get_overlap_cuboid(c)
            if oc:
                overlap += oc.size()

        return overlap

    def size(self):
        return ((self.xf + 1) - self.xi) * ((self.yf + 1) - self.yi) * ((self.zf + 1) - self.zi)
