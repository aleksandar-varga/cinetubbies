import ImageHelper from '@/helpers/image-helper';

export class OfficialProp {
  constructor(data) {
    _.assign(this, data);

    if (this.image) {
      this.image.path = ImageHelper.getAbsolutePath(this.image.path);
    }
  }

  update(data) {
    _.assign(this, data);
  }
};
