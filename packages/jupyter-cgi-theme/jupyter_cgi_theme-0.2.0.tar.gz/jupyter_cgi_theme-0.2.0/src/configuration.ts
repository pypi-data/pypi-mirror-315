export type Links = Array<{ label: string; href: string }>;

export type AppConfig = {
  appName: string;
  header: {
    isVisible: boolean;
    insulaAppsMenuLinks: Links;
    otherInfoMenuLinks: Links;
  };
};

export const appConfig: AppConfig = {
  appName: 'Insula Experiment',
  header: {
    isVisible: true,
    insulaAppsMenuLinks: [
      {
        label: 'Awareness',
        href: 'https://insula.destine.eu/advanced'
      },
      {
        label: 'Intellect',
        href: 'https://insula.destine.eu/sir'
      },
      {
        label: 'Perception',
        href: 'https://insula.destine.eu/dama'
      }
    ],
    otherInfoMenuLinks: [
      {
        label: 'Docs',
        href: 'https://platform.destine.eu/services/documents-and-api/doc/?service_name=insula'
      },
      {
        label: 'Support',
        href: 'https://platform.destine.eu/support/'
      }
    ]
  }
};
