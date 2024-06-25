using System.ComponentModel.DataAnnotations;

namespace Mayo_Clinic.ViewModels
{
    public class DisplayPatientViewModel
    {
        public int Id { get; set; }
        public string Name { get; set; }
        [Display(Name = "Phone Number")]
        public string PhoneNumber { get; set; } = string.Empty;
        public int Age { get; set; }
        public string Classification { get; set; }
    }
}
