from datetime import datetime, timedelta
from civipy.base import CiviCRMBase
from civipy.contribution import CiviContribution


class CiviMembershipPayment(CiviCRMBase):
    pass


class CiviMembership(CiviCRMBase):
    def payments(self):
        """Find all MembershipPayment records associated with this Membership."""
        return CiviMembershipPayment.find_all(membership_id=self.id)

    def apply_contribution(self, contribution: CiviContribution):
        """Apply a Contribution to this Membership and extend the expiration date."""
        # The new expiration date should be the old expiration date plus one year.
        end = datetime.strptime(self.end_date, "%Y-%m-%d")
        end = end.replace(year=end.year + 1)
        # If the new expiration date is in the future, change the status to "Current".
        status = "2" if end > datetime.now() else self.status_id
        cid = contribution.id
        CiviMembershipPayment.create(contribution_id=cid, membership_id=self.id)
        self.update(end_date=end.strftime("%Y-%m-%d"), status_id=status)
