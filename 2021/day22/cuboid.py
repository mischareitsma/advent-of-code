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
        return False

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

        # Returns depend on the type of overlap: corner chipped off, a resulting
        # 'stair' or a 'plane'
        # Even more complex, can also chip from the middle, or cut in half

        # Returning 3 cuboids:
        # 1 original xrange, z range, trimmed y range
        # 2 original xrange, trimmed z range, overlapping y range
        # 3 trimmed xrange, overlapping z and y range
        trim_xi ,trim_xf = self.get_trimmed_range(self.xi, self.xf, other.xi, other.xf)
        trim_yi, trim_yf = self.get_trimmed_range(self.yi, self.yf, other.yi, other.yf)
        trim_zi, trim_zf = self.get_trimmed_range(self.zi, self.zf, other.zi, other.zf)



        return reduce_cuboid_list(spit_cuboids), True

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
                overlap += ((oc.xf + 1) - oc.xi) * ((oc.yf + 1) - oc.yi) * ((oc.zf + 1) - oc.zi)

        return overlap
